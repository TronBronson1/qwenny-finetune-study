"""Profile existing candidate messages; do not promote them into approved training data."""
import hashlib,json,pathlib
from transformers import AutoTokenizer

ROOT=pathlib.Path(__file__).resolve().parent
EXP=ROOT.parent
REV='c202236235762e1c871ad0ccb60c8ee5ba337b9a'
tok=AutoTokenizer.from_pretrained(ROOT/'checkpoint'/REV,local_files_only=True)
system=(EXP/'prompt-comparison'/'SYSTEM_PROMPT.txt').read_text(encoding='utf-8-sig')
report={'revision':REV,'review_status':'candidates only; independent review pending','rows':[]}
for task in ['D01','D02']:
    folder=EXP/'prompt-comparison'/'demonstrations'/task
    spec=(folder/'SPEC.md').read_text(encoding='utf-8-sig')
    answer=(folder/'ANSWER.md').read_text(encoding='utf-8-sig')
    messages=[{'role':'system','content':system},{'role':'user','content':spec},{'role':'assistant','content':answer}]
    rendered=tok.apply_chat_template(messages,tokenize=False,enable_thinking=False)
    encoded=tok(rendered,add_special_tokens=False)['input_ids']
    assert len(encoded)>len(tok.encode(answer,add_special_tokens=False))
    report['rows'].append({'id':task,'family':{'D01':'integer-ceiling-division','D02':'literal-prefix-removal'}[task],
        'chat_tokens_thinking_disabled':len(encoded),'answer_tokens':len(tok.encode(answer,add_special_tokens=False)),
        'source_sha256':{f:hashlib.sha256((folder/f).read_bytes()).hexdigest() for f in ['SPEC.md','ANSWER.md']}})
report['total_tokens']=sum(r['chat_tokens_thinking_disabled'] for r in report['rows'])
report['max_tokens']=max(r['chat_tokens_thinking_disabled'] for r in report['rows'])
report['note']='Length profile only. Thinking disabled is an explicit candidate formatting setting, not a change to historical inference controls. No data exported or trained.'
(ROOT/'candidate-token-profile.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
