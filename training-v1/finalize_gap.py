"""Assemble the completed development investigation without loading a model."""
import hashlib,json,pathlib

ROOT=pathlib.Path(__file__).resolve().parent
p=ROOT/'investigations/gap-001'
def read(path): return json.loads(path.read_text(encoding='utf-8'))
def write(path,value): path.write_text(json.dumps(value,indent=2),encoding='utf-8')
run=read(p/'report.json'); assert run['status']=='completed' and len(run['completed'])==8
scored=read(ROOT/'scoring/gap-001/summary.json')['results']
assert all(not r['provisional_executable_pass'] for r in scored)
reasons={
 'DV001/base-greedy-0':'Correct implementation: 13 passed, 1 failed. A normal tuple is wrongly classified as a rejected tuple subclass.',
 'DV001/epoch-5-greedy-0':'Truncated at 2048 tokens inside an enormous integer; no complete code block. Earlier negative and wrapping expected rotations are also wrong.',
 'DV001/base-sample-0':'Correct implementation: 14 passed, 4 failed. Wrong large/negative rotation values and normal-tuple rejection.',
 'DV001/epoch-5-sample-0':'Correct implementation: 6 passed, 2 failed. Wrong expected values for negative rotation, including -100 modulo 3.',
 'DV002/epoch-5-greedy-0':'Truncated at 2048 tokens while enumerating valid times; no complete code block or assertions.',
 'DV002/base-sample-0':'Correct implementation: 17 passed, 1 failed. Invalid-type cases contain inconsistent tuple lengths, causing unpacking failure. Exact built-in return type and str-subclass coverage are also absent.',
 'DV002/epoch-5-sample-0':'Syntax error during collection. Source also expects None for valid/invalid times and rejected types instead of required integer values/exceptions.',
 'DV002/base-greedy-0':'Truncated at 2048 tokens with an unfinished function and no closed code block. Earlier tests both accept and reject valid 01:59.',
}
reviews=[]
for row in scored:
 key=row['task']+'/'+row['variant']; answer=p/key/'answer.md'
 reviews.append(dict(task=row['task'],variant=row['variant'],strict_accepted=False,
  reason=reasons[key],answer_sha256=hashlib.sha256(answer.read_bytes()).hexdigest(),
  review_scope='Definitive rejection; exhaustive missing-category audit is unnecessary after reference/syntax/completion failure.'))
write(ROOT/'scoring/gap-001/agent-acceptance-review.json',reviews)
inspections=read(p/'code_inspections.json')
inspections['DV002/base-sample-0']['notes']='Read entire source: subject/pytest only, bounded loops. Inconsistent case tuple lengths cause unpacking failure; no exact-int or str-subclass check.'
write(p/'code_inspections.json',inspections)
old=read(ROOT/'scoring/qwenny-001-direct-001/summary.json')['results']
cells=[]
for row in scored:
 cells.append(dict(task=row['task'],model='epoch-5' if row['variant'].startswith('epoch-5') else 'base',decoder='greedy-0' if 'greedy' in row['variant'] else 'sample-0',strict_accepted=False,reference_valid=row.get('reference_valid',False),truncated=row['truncated'],source='scoring/gap-001',variant=row['variant']))
for row in old:
 if row['variant'] in ('base-A','epoch-5-C'):
  assert not row['provisional_executable_pass']
  cells.append(dict(task=row['task'],model='base' if row['variant']=='base-A' else 'epoch-5',decoder='sample-1.5',strict_accepted=False,reference_valid=row.get('reference_valid',False),truncated=row['truncated'],source='scoring/qwenny-001-direct-001',variant=row['variant']))
assert len(cells)==12
summary=dict(status='completed',scope='Two visible development families, one seed; direct-answer investigation, not final evaluation.',new_answers=8,reused_answers=4,new_strict_accepted=0,new_reference_valid=0,new_truncations=3,cells=cells,likelihood=read(p/'likelihood-summary.json'),loss_decomposition=read(p/'loss-decomposition.json'),training_performed=False,final_test_used=False,limitations=['No thinking-enabled control','Not a full decoder factorial','No precision or long-cache causal comparison','No general aptitude conclusion'])
write(p/'RESULTS.json',summary)
manifest={}
for folder in (p,ROOT/'scoring/gap-001'):
 for f in sorted(folder.rglob('*')):
  if f.is_file() and f.name!='SHA256SUMS.json': manifest[str(f.relative_to(ROOT))]=hashlib.sha256(f.read_bytes()).hexdigest()
write(p/'SHA256SUMS.json',manifest)
print(json.dumps({k:summary[k] for k in ('status','new_answers','reused_answers','new_strict_accepted','new_reference_valid','new_truncations')},indent=2))
