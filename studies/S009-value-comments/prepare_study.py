"""S009 fail-closed, local-only packet export and exact supervised token preparation."""
import ast, copy, hashlib, importlib.util, json, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
EXP = HERE.parents[1]
DATA = EXP / 'dataset-v1/candidate-007'
sys.path.insert(0, str(EXP / 'training-v1'))

SELECTED = ('TR007', 'TR010', 'TR038', 'TR049')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(p,v): p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def rows(p): return [json.loads(s) for s in p.read_text(encoding='utf-8').splitlines()]
def write_rows(p,rs): p.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rs),encoding='utf-8')
def code(answer):
    blocks=re.findall(r'```python\s*\n(.*?)```',answer,re.S)
    assert len(blocks)==1
    return blocks[0]
def normalized(source):
    tree=ast.parse(source)
    for n in ast.walk(tree):
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='pytest' and n.func.attr=='param':
            n.keywords=[k for k in n.keywords if k.arg!='id']
    return ast.dump(tree,include_attributes=False)
def load_function(path,name):
    spec=importlib.util.spec_from_file_location('s009_'+sha(path),path)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return getattr(module,name)
def calculation(ident,args):
    if ident=='TR007':
        return '+'.join(str(int(c)) for c in str(args[0]))
    if ident=='TR010':
        # Enumerating set-bit powers avoids a 101-term zero-filled expression.
        n=args[0]; powers=[str(i) for i in range(n.bit_length()) if n & (1<<i)]
        return '0' if not powers else ' + '.join('1' for _ in powers)
    if ident=='TR038':
        a,b=(int(c,16) for c in args[0]); return f'{a}*16+{b}'
    if ident=='TR049':
        r,c,_,width=args; return f'{r}*{width}+{c}'
    raise AssertionError(ident)
def safe_arithmetic(expr):
    tree=ast.parse(expr,mode='eval')
    assert all(isinstance(n,(ast.Expression,ast.BinOp,ast.Add,ast.Mult,ast.Constant,ast.Load)) for n in ast.walk(tree))
    assert all(type(n.value) is int for n in ast.walk(tree) if isinstance(n,ast.Constant))
    return eval(compile(tree,'<verified arithmetic>','eval'),{'__builtins__':{}})

def verify_inputs():
    handoff=read(EXP/'program/handoffs/controlled-training-001.json')
    checks={}
    for name,expected in handoff['immutable_source_sha256'].items():
        actual=sha(EXP/name); assert actual==expected,name; checks[name]=actual
    hashes=read(DATA/'SHA256.json')
    for name,expected in hashes.items(): assert sha(DATA/name)==expected,name
    cert=read(EXP/'studies/S007-measurement-repair/calibration-certificate.json')
    assert cert['status']=='passed' and cert['final_candidate_hash']==sha(DATA/'SHA256.json')
    return dict(handoff_sources=checks,candidate_files_verified=len(hashes),candidate_manifest_sha256=sha(DATA/'SHA256.json'))

def main():
    from prepare_data import encode_answer, CHECKPOINT, REV
    from transformers import AutoTokenizer
    out=HERE/'preparation-001'; assert not out.exists()
    verification=verify_inputs()
    original=rows(DATA/'model-packets/training-requests.jsonl')
    assert [r['id'] for r in original]==[f'TR{i:03}' for i in range(1,61)]
    baseline=copy.deepcopy(original)
    overlay=EXP/'studies/S007-measurement-repair/length-preview-002/messages.json'
    baseline[57]['messages']=read(overlay)
    # Shared presentation compaction prospectively applied to the grid family.
    # Literal contents and all executable nodes must remain identical.
    grid=baseline[48]['messages'][-1]['content']; grid_code=code(grid)
    compact=re.sub(r', +',',',grid_code)
    assert ast.dump(ast.parse(grid_code))==ast.dump(ast.parse(compact))
    baseline[48]['messages'][-1]['content']=grid.replace(grid_code,compact,1)
    treatment=copy.deepcopy(baseline); comments=[]; provenance=[]
    manifest={r['id']:r for r in read(DATA/'manifest.json')['tasks']}
    for b,t,parent in zip(baseline,treatment,original):
        ident=b['id']; assert ident==t['id']==parent['id']
        task=DATA/'tasks/training'/ident
        if ident in SELECTED:
            source=code(b['messages'][-1]['content']); replacement=source
            ref=load_function(task/'evaluator/reference/subject.py',manifest[ident]['function'])
            oracle=load_function(task/'evaluator/oracle.py','oracle')
            for case in read(task/'evaluator/cases.json'):
                if 'expected_python' not in case: continue
                args=ast.literal_eval(case['args_python']); expected=ast.literal_eval(case['expected_python'])
                expr=calculation(ident,args); value=safe_arithmetic(expr)
                assert type(expected) is int and value==expected==oracle(*copy.deepcopy(args))==ref(*copy.deepcopy(args))
                pattern=r'(?m)^(.*pytest\.param\(.*id="'+case['id']+r'"\),)\s*$'
                annotation=f' # {expr} = {value}'
                if ident=='TR010':
                    positions=[i for i in range(args[0].bit_length()) if args[0] & (1<<i)]
                    annotation=f' # Set-bit positions {positions}: {expr} = {value}'
                replacement,n=re.subn(pattern,lambda m:m[1]+annotation,replacement)
                assert n==1,(ident,case['id'])
                comments.append(dict(task=ident,case=case['id'],args_python=case['args_python'],expression=expr,value=value,comment=annotation.strip(),oracle_sha256=sha(task/'evaluator/oracle.py'),reference_sha256=sha(task/'evaluator/reference/subject.py')))
            assert ast.dump(ast.parse(source))==ast.dump(ast.parse(replacement))
            t['messages'][-1]['content']=b['messages'][-1]['content'].replace(source,replacement,1)
        assert b['messages'][:-1]==t['messages'][:-1]
        assert normalized(code(b['messages'][-1]['content']))==normalized(code(t['messages'][-1]['content']))==normalized((task/'test_target.py').read_text(encoding='utf-8'))
        provenance.append(dict(id=ident,parent_record_sha256=digest(parent),baseline_record_sha256=digest(b),treatment_record_sha256=digest(t),overlay=ident=='TR058',comments_added=sum(c['task']==ident for c in comments),executable_ast_equal_ignoring_display_ids=True))
    tok=AutoTokenizer.from_pretrained(CHECKPOINT,local_files_only=True)
    encoded={arm:[encode_answer(tok,r['messages'],r['id'],2048) for r in records] for arm,records in [('baseline',baseline),('comments',treatment)]}
    # Retain the historical 12-task A/B loss interface; neither view enters training.
    demos=[]
    for ident in ('D01','D02'):
        folder=EXP/'prompt-comparison/demonstrations'/ident
        demos.extend([dict(role='user',content=(folder/'SPEC.md').read_text(encoding='utf-8').strip()),dict(role='assistant',content=(folder/'ANSWER.md').read_text(encoding='utf-8').strip())])
    development=[]
    for request in rows(DATA/'model-packets/development-requests.jsonl'):
        ident=request['id']; assert re.fullmatch(r'DV\d{3}',ident)
        target=(DATA/'tasks/development'/ident/'TARGET.md').read_text(encoding='utf-8')
        if ident=='DV008':
            escaped=target.replace('\u0301',r'\u0301')
            assert ast.dump(ast.parse(code(target)))==ast.dump(ast.parse(code(escaped)))
            target=escaped
        for view in ('A','B'):
            messages=request['messages'] if view=='A' else [request['messages'][0]]+demos+request['messages'][1:]
            record=encode_answer(tok,messages+[dict(role='assistant',content=target)],ident+'-'+view,16134)
            record.update(task_id=ident,arm=view); development.append(record)
    assert len(development)==24
    # No output is created until all input, expression, AST and token gates pass.
    out.mkdir()
    dump(out/'source-verification.json',verification); dump(out/'comments.json',comments); dump(out/'record-provenance.json',provenance)
    export_hashes={}
    for arm,records in [('baseline',baseline),('comments',treatment)]:
        folder=out/arm; folder.mkdir(); write_rows(folder/'messages.jsonl',records)
        write_rows(folder/'train.jsonl',encoded[arm]); write_rows(folder/'development.jsonl',development)
        export_hashes[arm]=sha(folder/'messages.jsonl')
        report=dict(status='passed',base_revision=REV,arm=arm,train_rows=60,development_rows=24,max_train_tokens=max(r['input_tokens'] for r in encoded[arm]),max_development_tokens=max(r['input_tokens'] for r in development),total_train_input_tokens=sum(r['input_tokens'] for r in encoded[arm]),total_train_target_tokens=sum(r['target_tokens'] for r in encoded[arm]),train_jsonl_sha256=sha(folder/'train.jsonl'),development_jsonl_sha256=sha(folder/'development.jsonl'),messages_jsonl_sha256=export_hashes[arm],no_truncation=True,decoded_target_matches_every_answer=True,prompt_and_empty_reasoning_markup_masked=True,development_policy='12 A/B no-gradient loss views only; excluded from optimizer records',shared_presentation_changes=['TR058 certified fit overlay','TR049 optional comma whitespace removed with exact AST equality','DV008 development target combining accent escaped as literal backslash-u0301 with exact AST equality to prevent tokenizer NFC normalization'])
        dump(folder/'report.json',report)
        for r in (encoded[arm][0],max(encoded[arm],key=lambda r:r['input_tokens'])):
            (folder/(r['id']+'-mask-review.txt')).write_text('MASKED PREFIX:\n'+tok.decode(r['input_ids'][:r['first_target_token']],skip_special_tokens=False)+'\nSUPERVISED:\n'+tok.decode([v for v in r['labels'] if v!=-100],skip_special_tokens=False),encoding='utf-8')
    dump(out/'authorization.json',dict(scope='S009 local preparation, validation, two fresh controlled training trajectories and matched testing under handoff boundaries',basis='User: Perfect you may proceed with the plan. Existing routine design/testing delegation recorded in handoff.',authored_comment_review='Agent authored and verified; no claim of user review of unseen exact text or independent acceptance',approved_export_hashes=export_hashes,approval_guard='Consumers must match this exact variant hash and prepared file hashes. Historical candidate-006 approval is not reused.',source_candidate_sha256=verification['candidate_manifest_sha256']))
    dump(out/'summary.json',dict(status='preparation-passed-not-training-authorized-by-gates',selected_training_families=SELECTED,comments=len(comments),source_verification=verification,variant_exports=export_hashes,script_sha256=sha(pathlib.Path(__file__)),remaining_gates=['all-reference/mutant runtime validation','model-suite v2 scorer calibration','frozen protocol and cost ceiling','actual GPU preflight','paired training and import verification']))
    print(json.dumps(dict(comments=len(comments),reports={arm:read(out/arm/'report.json') for arm in encoded}),indent=2))
if __name__=='__main__': main()
