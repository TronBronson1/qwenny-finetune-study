"""Versioned target-format ablation; preserve executable AST except pytest IDs."""
import argparse,ast,copy,hashlib,json,pathlib,re,shutil
from transformers import AutoTokenizer
from prepare_data import CHECKPOINT,ROOT,EXP,encode_answer

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,data): path.write_text(json.dumps(data,indent=2),encoding='utf-8')
def normalized(code):
    tree=ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and isinstance(node.func.value,ast.Name) and node.func.value.id=='pytest' and node.func.attr=='param':
            node.keywords=[k for k in node.keywords if k.arg!='id']
    return ast.dump(tree,include_attributes=False)

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--out',default='prepared-compact-001'); a=parser.parse_args()
    out=ROOT/a.out; assert out.parent==ROOT and not out.exists()
    source=EXP/'dataset-v1/training-approved-001'; old=ROOT/'prepared-001'
    prov=json.loads((source/'provenance.json').read_text()); before=json.loads((old/'report.json').read_text())
    assert sha(source/'train.jsonl')==prov['train_sha256']
    assert sha(old/'train.jsonl')==before['train_jsonl_sha256']
    assert sha(old/'development.jsonl')==before['development_jsonl_sha256']
    rows=[json.loads(line) for line in (source/'train.jsonl').read_text(encoding='utf-8').splitlines()]
    assert len(rows)==len(prov['training_ids'])==60
    tok=AutoTokenizer.from_pretrained(CHECKPOINT,local_files_only=True)
    fence=chr(96)*3; transformed=[]; encoded=[]; checks=[]
    prose='Cases map explicit argument tuples to expected values, exact types, post-state and required exceptions, including listed ordering witnesses. Coverage is finite, not exhaustive. No execution is claimed.'
    for ident,row in zip(prov['training_ids'],rows):
        text=row['messages'][-1]['content']; blocks=re.findall(fence+r'python\n(.*?)'+fence,text,re.S); assert len(blocks)==1
        original=blocks[0]
        compact=re.sub(r''',\s*id\s*=\s*(['"])[^'"\n]*\1''','',original)
        compact='\n'.join(line.rstrip() for line in compact.splitlines() if line.strip())+'\n'
        assert normalized(original)==normalized(compact),ident
        assert sum(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(original)))==sum(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(compact)))
        messages=copy.deepcopy(row['messages']); messages[-1]['content']=fence+'python\n'+compact+fence+'\n\n'+prose+'\n'
        assert messages[:-1]==row['messages'][:-1]
        record=encode_answer(tok,messages,ident,2048)
        original_record=encode_answer(tok,row['messages'],ident,2048)
        transformed.append({'messages':messages}); encoded.append(record)
        checks.append(dict(id=ident,normalized_ast_equal=True,original_code_sha256=hashlib.sha256(original.encode()).hexdigest(),compact_code_sha256=hashlib.sha256(compact.encode()).hexdigest(),original_target_tokens=original_record['target_tokens'],compact_target_tokens=record['target_tokens']))
    out.mkdir(); (out/'targets').mkdir()
    for ident,row in zip(prov['training_ids'],transformed):
        text=row['messages'][-1]['content']; folder=out/'targets'/ident; folder.mkdir()
        (folder/'TARGET.md').write_text(text,encoding='utf-8'); (folder/'test_target.py').write_text(re.findall(fence+r'python\n(.*?)'+fence,text,re.S)[0],encoding='utf-8')
    (out/'messages.jsonl').write_text(''.join(json.dumps(row,ensure_ascii=False)+'\n' for row in transformed),encoding='utf-8')
    (out/'train.jsonl').write_text(''.join(json.dumps(row)+'\n' for row in encoded),encoding='utf-8')
    shutil.copyfile(old/'development.jsonl',out/'development.jsonl')
    report=dict(before)
    report.update(status='prepared-awaiting-executable-validation',ablation='compact-target-format-001',source_prepared='prepared-001',source_messages_sha256=sha(source/'train.jsonl'),messages_sha256=sha(out/'messages.jsonl'),max_train_tokens=max(r['input_tokens'] for r in encoded),total_train_input_tokens=sum(r['input_tokens'] for r in encoded),total_train_target_tokens=sum(r['target_tokens'] for r in encoded),train_jsonl_sha256=sha(out/'train.jsonl'),development_jsonl_sha256=sha(out/'development.jsonl'),development_byte_identical=True,all_training_executable_ast_equal_ignoring_pytest_ids=True,transformations=['Remove pytest.param id display metadata','Remove blank lines/trailing spaces','Replace repeated mapping/limitations prose with shorter version'],unchanged=['System/user messages','All executable AST other than pytest display IDs','Task order and splits','Reference/mutant/final fixtures','Development target tokens'],per_task=checks)
    report['target_token_reduction_fraction']=1-report['total_train_target_tokens']/before['total_train_target_tokens']
    write(out/'report.json',report)
    shutil.copyfile(pathlib.Path(__file__),out/'prepare_compact.py')
    print(json.dumps({k:report[k] for k in ('status','max_train_tokens','total_train_input_tokens','total_train_target_tokens','target_token_reduction_fraction','development_byte_identical')},indent=2))

if __name__=='__main__': main()
