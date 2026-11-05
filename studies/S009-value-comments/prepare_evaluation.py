"""Freeze matched prompts without accessing final/regression tasks."""
import copy,json
from prepare_study import HERE,EXP,DATA,read,rows,dump,sha
IDS=('TR024','DV008','TR025','DV004','TR038','DV011','TR049','DV007')
def main():
    from transformers import AutoTokenizer
    import sys
    sys.path.insert(0,str(EXP/'training-v1'))
    from prepare_data import CHECKPOINT
    out=HERE/'inputs'; assert not out.exists(); out.mkdir()
    tok=AutoTokenizer.from_pretrained(CHECKPOINT,local_files_only=True)
    requests={r['id']:r for split in ('training','development') for r in rows(DATA/'model-packets'/(split+'-requests.jsonl'))}
    manifest={r['id']:r for r in read(DATA/'manifest.json')['tasks']}
    selection=[]
    for ident in IDS:
        record=manifest[ident]; messages=copy.deepcopy(requests[ident]['messages'][:2])
        assert [m['role'] for m in messages]==['system','user']
        if ident=='DV008':
            messages[-1]['content']+='\nA character means one Python Unicode code point. Do not normalize strings or treat a displayed grapheme cluster as one code point.\n'
        prompt=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=False)
        ids=tok(prompt,add_special_tokens=False)['input_ids']; assert len(ids)+2048<=16134
        folder=out/ident; folder.mkdir(); dump(folder/'messages.json',messages)
        (folder/'prompt.txt').write_text(prompt,encoding='utf-8'); dump(folder/'prompt-token-ids.json',ids)
        selection.append(dict(id=ident,split=record['split'],family=record['family'],function=record['function'],prompt_tokens=len(ids),prompt_sha256=sha(folder/'prompt.txt'),prompt_ids_sha256=sha(folder/'prompt-token-ids.json')))
    dump(HERE/'selection.json',dict(tasks=selection,selection='Same eight visible purposive tasks proposed in handoff; interleaved training/development. No new model outputs used.',unicode_clarification='DV008 inference-only explicit code-point/no-normalization wording; identical across inference arms; original archived results unchanged.'))
if __name__=='__main__': main()
