"""Pinned Qwenny runtime: NF4 frozen base, explicit CPU embedding, masked chunked loss."""
import gc, hashlib, json, os, pathlib, subprocess, threading, time, ctypes
import torch
from torch.utils.checkpoint import checkpoint
from transformers import AutoTokenizer, BitsAndBytesConfig, Qwen3_5ForConditionalGeneration
from peft import LoraConfig, get_peft_model

ROOT=pathlib.Path(__file__).resolve().parent
EXP=ROOT.parent
REV="c202236235762e1c871ad0ccb60c8ee5ba337b9a"
BASE="Qwen/Qwen3.5-9B"
CHECKPOINT=EXP/"lora-feasibility"/"checkpoint"/REV

class FrozenCPUEmbedding(torch.nn.Embedding):
    def forward(self,input_ids):
        return super().forward(input_ids.to(self.weight.device)).to(input_ids.device)

def tokenizer():
    return AutoTokenizer.from_pretrained(CHECKPOINT,local_files_only=True)

def verify_checkpoint():
    manifest=json.loads((CHECKPOINT/"source-manifest.json").read_text(encoding="utf-8"))
    assert manifest["sha"]==REV
    for record in manifest["siblings"]:
        name=record["rfilename"]
        if not (name.endswith((".json",".txt",".jinja",".safetensors")) or name=="LICENSE"): continue
        path=CHECKPOINT/name
        assert path.exists() and path.stat().st_size==record["size"],name
        if record.get("lfs",{}).get("sha256"):
            with path.open("rb") as f: actual=hashlib.file_digest(f,"sha256").hexdigest()
            assert actual==record["lfs"]["sha256"],name

def load_base(training=False):
    assert torch.cuda.is_available()
    free,total=torch.cuda.mem_get_info()
    assert free>=8*1024**3,"Less than 8 GiB initially available; no model load attempted"
    quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type="nf4",bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=torch.bfloat16)
    model=Qwen3_5ForConditionalGeneration.from_pretrained(CHECKPOINT,local_files_only=True,quantization_config=quant,dtype=torch.bfloat16,device_map={"":0},attn_implementation="sdpa",trust_remote_code=False)
    original=model.get_input_embeddings()
    cpu=FrozenCPUEmbedding.from_pretrained(original.weight.detach().cpu(),freeze=True,padding_idx=original.padding_idx)
    model.set_input_embeddings(cpu); del original
    protected={id(p) for m in [model.get_input_embeddings(),model.get_output_embeddings()] for p in m.parameters()}
    for p in model.parameters():
        p.requires_grad_(False)
        if id(p) not in protected and p.dtype in (torch.float16,torch.bfloat16) and p.__class__.__name__!="Params4bit":
            p.data=p.data.to(torch.float32)
    model.config.use_cache=False
    model.config.text_config.use_cache=False
    if training: model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant":False})
    gc.collect(); torch.cuda.synchronize(); torch.cuda.empty_cache()
    return model

def attach_lora(model):
    targets=[n for n,_ in model.named_modules() if ".language_model." in "."+n and n.endswith((".self_attn.q_proj",".self_attn.v_proj"))]
    assert len(targets)==16
    model=get_peft_model(model,LoraConfig(r=4,lora_alpha=8,lora_dropout=0.,bias="none",target_modules=targets,task_type="CAUSAL_LM"))
    trainable={n:p for n,p in model.named_parameters() if p.requires_grad}
    assert sum(p.numel() for p in trainable.values())==557056
    assert all("lora_" in n for n in trainable)
    return model,trainable,targets

def tensors(record):
    ids=torch.tensor([record["input_ids"]],device="cuda",dtype=torch.long)
    labels=torch.tensor([record["labels"]],device="cuda",dtype=torch.long)
    return ids,torch.ones_like(ids),labels

def masked_loss(network,ids,attention,labels,chunk=128):
    core=network.get_base_model()
    hidden=core.model(input_ids=ids,attention_mask=attention,use_cache=False).last_hidden_state
    valid=(labels[:,1:]!=-100).sum()
    assert valid.item()>0,"No next-token assistant labels"
    def piece(h,target):
        logits=core.lm_head(h).float()
        return torch.nn.functional.cross_entropy(logits.reshape(-1,logits.shape[-1]),target.reshape(-1),ignore_index=-100,reduction="sum")
    parts=[]
    for start in range(0,ids.shape[1]-1,chunk):
        end=min(start+chunk,ids.shape[1]-1)
        target=labels[:,start+1:end+1]
        if not torch.any(target!=-100).item(): continue
        if torch.is_grad_enabled() and network.training:
            parts.append(checkpoint(piece,hidden[:,start:end,:],target,use_reentrant=False))
        else: parts.append(piece(hidden[:,start:end,:],target))
    return torch.stack(parts).sum()/valid

def memory():
    torch.cuda.synchronize()
    free,total=torch.cuda.mem_get_info()
    return dict(unix_time=time.time(),allocated=torch.cuda.memory_allocated(),reserved=torch.cuda.memory_reserved(),peak_allocated=torch.cuda.max_memory_allocated(),peak_reserved=torch.cuda.max_memory_reserved(),cuda_free=free,total=total)

class Monitor:
    def __init__(self,out):
        self.out=out; self.stop=threading.Event()
        self.keep_awake=False
        if os.name=='nt':
            ctypes.windll.kernel32.SetThreadExecutionState.argtypes=[ctypes.c_uint]
            ctypes.windll.kernel32.SetThreadExecutionState.restype=ctypes.c_uint
            self.keep_awake=bool(ctypes.windll.kernel32.SetThreadExecutionState(0x80000001))
        (out/'power-state.json').write_text(json.dumps({'temporary_system_required':self.keep_awake,'scope':'Current experiment process only; no persistent power-plan or display setting changed.'}),encoding='utf-8')
        self.log=(out/"windows-monitor.log").open("w")
        self.process=subprocess.Popen(["pwsh","-NoProfile","-NonInteractive","-File",str(EXP/"lora-feasibility"/"monitor-process-memory.ps1"),"-TrialPid",str(os.getpid()),"-OutputPath",str(out/"windows-process-memory.csv")],stdout=self.log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
        self.thread=threading.Thread(target=self.sample,daemon=True); self.thread.start()
    def sample(self):
        with (self.out/"gpu-memory.csv").open("w",encoding="utf-8") as f:
            f.write("unix_time,used_MiB,free_MiB,total_MiB\n")
            while not self.stop.is_set():
                r=subprocess.run(["nvidia-smi","--query-gpu=memory.used,memory.free,memory.total","--format=csv,noheader,nounits"],capture_output=True,text=True)
                f.write(f"{time.time()},{r.stdout.strip()}\n"); f.flush()
                self.stop.wait(.5)
    def close(self):
        self.stop.set(); self.thread.join(timeout=5)
        if self.process.poll() is None:
            self.process.terminate()
            try: self.process.wait(timeout=5)
            except subprocess.TimeoutExpired: self.process.kill()
        self.log.close()
        if self.keep_awake: ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
