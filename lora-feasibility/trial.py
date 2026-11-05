"""Disposable synthetic training plumbing check; never use this adapter for evaluation."""
import argparse, gc, hashlib, importlib.metadata, json, math, pathlib, subprocess, time, traceback, threading, os

BASE = 'Qwen/Qwen3.5-9B'
REV = 'c202236235762e1c871ad0ccb60c8ee5ba337b9a'
ROOT = pathlib.Path(__file__).resolve().parent
CHECKPOINT=ROOT/'checkpoint'/REV

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--run', required=True, help='New output directory, must not exist')
    p.add_argument('--seq', type=int, default=128)
    p.add_argument('--loss-chunk', type=int, default=0, help='Checkpoint vocabulary loss in token chunks; zero uses standard model loss')
    p.add_argument('--steps',type=int,default=1)
    p.add_argument('--windows-memory',action='store_true')
    p.add_argument('--cpu-embedding',action='store_true',help='Keep only the frozen input embedding in CPU RAM; transformer/head/adapters remain on CUDA')
    a = p.parse_args()
    out = pathlib.Path(a.run).resolve(); out.mkdir(parents=True, exist_ok=False)
    report = dict(base=BASE, revision=REV, sequence=a.seq, batch=1, rank=4,
                  status='started', purpose='synthetic plumbing only', stages=[])
    report['loss_chunk']=a.loss_chunk
    report['requested_steps']=a.steps
    report['process_id']=os.getpid()
    report['cpu_embedding_requested']=a.cpu_embedding
    assert a.steps>0
    def save():
        (out/'report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    save()
    windows_monitor=None
    if a.windows_memory:
        windows_monitor=subprocess.Popen(['pwsh','-NoProfile','-NonInteractive','-File',str(ROOT/'monitor-process-memory.ps1'),'-TrialPid',str(os.getpid()),'-OutputPath',str(out/'windows-process-memory.csv')],stdout=(out/'windows-monitor.log').open('w'),stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
    stop = threading.Event()
    def sample_gpu():
        with (out/'gpu-memory.csv').open('w',encoding='utf-8') as f:
            f.write('unix_time,used_MiB,free_MiB,total_MiB\n')
            while not stop.is_set():
                r=subprocess.run(['nvidia-smi','--query-gpu=memory.used,memory.free,memory.total','--format=csv,noheader,nounits'],capture_output=True,text=True)
                f.write(f'{time.time()},{r.stdout.strip()}\n'); f.flush()
                stop.wait(0.5)
    monitor=threading.Thread(target=sample_gpu,daemon=True); monitor.start()
    try:
        import torch
        from torch.utils.checkpoint import checkpoint
        from transformers import AutoTokenizer, Qwen3_5ForConditionalGeneration, BitsAndBytesConfig
        from peft import LoraConfig, get_peft_model, PeftModel
        report['packages'] = {x:importlib.metadata.version(x) for x in ['torch','transformers','peft','accelerate','bitsandbytes']}
        subprocess.run([__import__('sys').executable,'-m','pip','freeze'], stdout=(out/'packages.lock.txt').open('w'), check=True)
        assert torch.cuda.is_available(), 'CUDA unavailable'
        torch.manual_seed(42); torch.cuda.manual_seed_all(42)
        report['gpu'] = torch.cuda.get_device_name(0)
        report['capability'] = torch.cuda.get_device_capability(0)
        report['cuda_runtime'] = torch.version.cuda
        free, total = torch.cuda.mem_get_info(); report['initial_free_bytes']=free; report['total_bytes']=total
        assert free >= 8 * 1024**3, 'Unload inference model first: less than 8 GiB free; no model load attempted'
        torch.cuda.reset_peak_memory_stats()
        def stage(name):
            torch.cuda.synchronize()
            free, total = torch.cuda.mem_get_info()
            report['stages'].append(dict(name=name, unix_time=time.time(),allocated=torch.cuda.memory_allocated(), reserved=torch.cuda.memory_reserved(), peak_allocated=torch.cuda.max_memory_allocated(), peak_reserved=torch.cuda.max_memory_reserved(), free=free))
            save()
        assert CHECKPOINT.is_dir(), 'Run download_direct.py first'
        manifest=json.loads((CHECKPOINT/'source-manifest.json').read_text(encoding='utf-8'))
        assert manifest['sha']==REV
        for info in manifest['siblings']:
            name=info['rfilename']
            if not (name.endswith(('.json','.txt','.jinja','.safetensors')) or name=='LICENSE'): continue
            f=CHECKPOINT/name
            assert f.exists() and f.stat().st_size==info['size'], f'Incomplete checkpoint: {name}'
            if info.get('lfs',{}).get('sha256'):
                with f.open('rb') as stream: digest=hashlib.file_digest(stream,'sha256').hexdigest()
                assert digest==info['lfs']['sha256'], f'Checkpoint hash mismatch: {name}'
        report['checkpoint_path']=str(CHECKPOINT)
        tok = AutoTokenizer.from_pretrained(CHECKPOINT, local_files_only=True, trust_remote_code=False)
        tok.save_pretrained(out/'tokenizer')
        template = tok.chat_template
        report['chat_template_sha256'] = hashlib.sha256(str(template).encode()).hexdigest()
        quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type='nf4', bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.bfloat16)
        def load_base():
            base=Qwen3_5ForConditionalGeneration.from_pretrained(CHECKPOINT, local_files_only=True, quantization_config=quant, dtype=torch.bfloat16, device_map={'':0}, attn_implementation='sdpa', trust_remote_code=False)
            if a.cpu_embedding:
                base.eval()
                probe=torch.tensor([[42,43,44,45]],device='cuda')
                with torch.no_grad(),torch.autocast('cuda',dtype=torch.bfloat16):
                    expected_probe=base(input_ids=probe,use_cache=False,logits_to_keep=1).logits.float().cpu()
                class FrozenCPUEmbedding(torch.nn.Embedding):
                    def forward(self,input_ids):
                        destination=input_ids.device
                        return super().forward(input_ids.to(self.weight.device)).to(destination)
                original=base.get_input_embeddings()
                name=next(n for n,m in base.named_modules() if m is original)
                replacement=FrozenCPUEmbedding.from_pretrained(original.weight.detach().cpu(),freeze=True,padding_idx=original.padding_idx)
                base.set_input_embeddings(replacement)
                report['cpu_embedding']={'module':name,'device':str(replacement.weight.device),'dtype':str(replacement.weight.dtype),'parameters':replacement.weight.numel(),'weight_bytes':replacement.weight.numel()*replacement.weight.element_size(),'policy':'Explicit CPU lookup with output copied to input device. Initial load device_map describes loading, not this manual post-load placement.'}
                del original
                gc.collect(); torch.cuda.synchronize(); torch.cuda.empty_cache()
                with torch.no_grad(),torch.autocast('cuda',dtype=torch.bfloat16):
                    actual_probe=base(input_ids=probe,use_cache=False,logits_to_keep=1).logits.float().cpu()
                difference=(expected_probe-actual_probe).abs().max().item()
                report.setdefault('embedding_offload_equivalence',[]).append({'tokens':4,'last_token_max_abs_difference':difference})
                assert torch.equal(expected_probe,actual_probe),'CPU embedding changed probe logits'
                del probe,expected_probe,actual_probe
            return base
        report['phase']='base_load'; save()
        model = load_base(); model.config.use_cache=False
        stage('base_loaded')
        def prepare(base, checkpointing):
            # Same freezing/non-reentrant checkpointing protocol as PEFT, with an
            # explicit exception for the two huge frozen BF16 matrices. Do not
            # temporarily upcast them: that transient alone could cause an OOM.
            protected={id(p) for m in [base.get_input_embeddings(),base.get_output_embeddings()] for p in m.parameters()}
            for p in base.parameters():
                p.requires_grad_(False)
                if id(p) not in protected and p.dtype in (torch.float16,torch.bfloat16) and p.__class__.__name__!='Params4bit':
                    p.data=p.data.to(torch.float32)
            if checkpointing:
                base.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False})
            torch.cuda.empty_cache()
            return base
        model=prepare(model,True)
        report['unquantized_matrix_policy']='selective k-bit preparation: frozen input embeddings and lm_head stay BF16; other nonquantized FP16/BF16 weights upcast to FP32'
        # Only the eight full-attention blocks: no vision, MLP, embedding or DeltaNet adapters.
        targets = [n for n,m in model.named_modules() if '.language_model.' in '.'+n and n.endswith(('.self_attn.q_proj','.self_attn.v_proj'))]
        assert len(targets)==16, f'Unexpected architecture: {targets}'
        report['target_modules']=targets
        model=get_peft_model(model, LoraConfig(r=4,lora_alpha=8,lora_dropout=0.0,bias='none',target_modules=targets,task_type='CAUSAL_LM'))
        trainable={n:p for n,p in model.named_parameters() if p.requires_grad}
        assert trainable and all('lora_' in n for n in trainable)
        report['trainable']={n:list(p.shape) for n,p in trainable.items()}
        report['trainable_parameters']=sum(p.numel() for p in trainable.values())
        text=tok.apply_chat_template([{'role':'user','content':'Repeat the word blue.'},{'role':'assistant','content':'blue'}],tokenize=False,enable_thinking=False)
        ids=tok(text,add_special_tokens=False)['input_ids']
        # Repeated synthetic tokens fill exactly the requested length. Full-token loss is intentional here.
        ids=(ids*math.ceil(a.seq/len(ids)))[:a.seq]
        batch=torch.tensor([ids],device='cuda'); mask=torch.ones_like(batch)
        optimizer=torch.optim.AdamW(trainable.values(),lr=1e-4)
        def chunked_loss(network, ids, attention, chunk):
            core=network.get_base_model()
            hidden=core.model(input_ids=ids,attention_mask=attention,use_cache=False).last_hidden_state
            def piece(h,targets):
                logits=core.lm_head(h).float()
                return torch.nn.functional.cross_entropy(logits.reshape(-1,logits.shape[-1]),targets.reshape(-1),reduction='sum')
            parts=[]
            for start in range(0,ids.shape[1]-1,chunk):
                end=min(start+chunk,ids.shape[1]-1)
                parts.append(checkpoint(piece,hidden[:,start:end,:],ids[:,start+1:end+1],use_reentrant=False))
            return torch.stack(parts).sum()/(ids.shape[0]*(ids.shape[1]-1))
        if a.loss_chunk:
            assert a.loss_chunk>0
            model.train()
            probe=batch[:,:64]; probe_mask=mask[:,:64]
            with torch.autocast('cuda',dtype=torch.bfloat16):
                reference_loss=model(input_ids=probe,attention_mask=probe_mask,labels=probe).loss
            reference_loss.backward()
            reference_grads={n:p.grad.detach().float().cpu().clone() for n,p in trainable.items() if p.grad is not None}
            reference_value=reference_loss.item()
            optimizer.zero_grad(set_to_none=True)
            with torch.autocast('cuda',dtype=torch.bfloat16):
                checked_loss=chunked_loss(model,probe,probe_mask,min(32,a.loss_chunk))
            checked_loss.backward()
            norm=sum(g.square().sum().item() for g in reference_grads.values())**0.5
            diff=sum((p.grad.detach().float().cpu()-reference_grads[n]).square().sum().item() for n,p in trainable.items() if n in reference_grads)**0.5
            report['chunk_validation']={'tokens':probe.shape[1],'standard_loss':reference_value,'chunked_loss':checked_loss.item(),'gradient_relative_l2_difference':diff/max(norm,1e-12)}
            assert abs(reference_value-checked_loss.item())<1e-3
            assert diff/max(norm,1e-12)<0.03, 'Chunked gradient disagreement'
            optimizer.zero_grad(set_to_none=True)
            del probe,probe_mask,reference_loss,checked_loss,reference_grads
            gc.collect(); torch.cuda.synchronize(); torch.cuda.empty_cache()
            report['validation_peak_allocated']=torch.cuda.max_memory_allocated()
            torch.cuda.reset_peak_memory_stats()
        model.train(); stage('adapter_ready')
        report['updates']=[]
        for update in range(a.steps):
            suffix=f':{update+1}' if a.steps>1 else ''
            report['phase']='forward'+suffix; save()
            start=time.monotonic()
            with torch.autocast('cuda',dtype=torch.bfloat16):
                loss=chunked_loss(model,batch,mask,a.loss_chunk) if a.loss_chunk else model(input_ids=batch,attention_mask=mask,labels=batch).loss
            assert torch.isfinite(loss), 'Nonfinite loss'
            report['loss']=loss.item(); stage('forward'+suffix)
            report['phase']='backward'+suffix; save()
            loss.backward(); stage('backward'+suffix)
            grads={n:p.grad for n,p in model.named_parameters() if p.grad is not None}
            assert grads and all(n in trainable for n in grads), 'Unexpected base gradient'
            assert all(torch.isfinite(g).all().item() for g in grads.values()), 'Nonfinite gradients'
            assert any(torch.count_nonzero(g).item()>0 for g in grads.values()), 'All gradients zero'
            report['gradient_parameters']=list(grads)
            before={n:p.detach().cpu().clone() for n,p in trainable.items()}
            report['phase']='optimizer'+suffix; save()
            optimizer.step(); optimizer.zero_grad(set_to_none=True); stage('optimizer'+suffix)
            assert any(not torch.equal(before[n],p.detach().cpu()) for n,p in trainable.items()), 'No parameter updated'
            report['updates'].append({'step':update+1,'loss':loss.item(),'seconds':time.monotonic()-start})
        report['step_seconds']=sum(u['seconds'] for u in report['updates'])
        model.save_pretrained(out/'adapter',safe_serialization=True)
        model.eval()
        with torch.no_grad(), torch.autocast('cuda',dtype=torch.bfloat16): expected=model(input_ids=batch,attention_mask=mask,logits_to_keep=1).logits[:,-1,:].float().cpu()
        del loss,grads,trainable,optimizer,model; gc.collect(); torch.cuda.empty_cache(); stage('released')
        report['phase']='reload'; save()
        reload_base=load_base()
        reload_base=prepare(reload_base,False)
        reloaded=PeftModel.from_pretrained(reload_base,out/'adapter',is_trainable=False); reloaded.eval()
        with torch.no_grad(), torch.autocast('cuda',dtype=torch.bfloat16): actual=reloaded(input_ids=batch,attention_mask=mask,logits_to_keep=1).logits[:,-1,:].float().cpu()
        report['reload_max_abs_diff']=(expected-actual).abs().max().item()
        assert torch.allclose(expected,actual,atol=0.02,rtol=0.01), 'Reload logits mismatch'
        stage('reloaded'); report['status']='passed'
    except BaseException as e:
        report['status']='interrupted' if isinstance(e,KeyboardInterrupt) else 'failed'; report['error']=repr(e)
        try:
            report['failure_memory']={'peak_allocated':torch.cuda.max_memory_allocated(),'peak_reserved':torch.cuda.max_memory_reserved(),'free_total':torch.cuda.mem_get_info()}
        except Exception:
            pass
        (out/'traceback.txt').write_text(traceback.format_exc(),encoding='utf-8')
        raise
    finally:
        stop.set(); monitor.join(timeout=5)
        save()

if __name__=='__main__': main()
