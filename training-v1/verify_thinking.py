"""Read-only consistency checks for the six predeclared thinking cells."""
import hashlib, json
from pathlib import Path

root=Path(__file__).resolve().parent
out=root/'probes/thinking-001'
report=json.loads((out/'report.json').read_text())
assert report['status']=='completed'
assert len(report['completed'])==6
expected={(t,v) for t in ('DV001','DV002') for v in ('base','original-e5','compact-e5')}
assert {(r['task'],r['variant']) for r in report['completed']}==expected
provenance=json.loads((out/'provenance.json').read_text())
for name,digest in provenance['input_sha256'].items():
    path=root.parent/Path(name)
    assert hashlib.sha256(path.read_bytes()).hexdigest()==digest, name
for task in ('DV001','DV002'):
    rows=[r for r in report['completed'] if r['task']==task]
    assert len({r['prompt_sha256'] for r in rows})==1
    assert len({r['prompt_tokens'] for r in rows})==1
    for row in rows:
        folder=out/task/row['variant']
        ids=json.loads((folder/'output_token_ids.json').read_text())
        assert len(ids)==row['generated_tokens']<=8192
        assert row['prompt_tokens']+8192<=16134
        assert hashlib.sha256((folder/'prompt.txt').read_text(encoding='utf-8').encode()).hexdigest()==row['prompt_sha256']
        raw=(folder/'output.raw.txt').read_text(encoding='utf-8')
        assert row['thinking_closed']==('</think>' in raw)
        assert not row['truncated'] or len(ids)==8192
        assert row['terminated'] != row['truncated']
        if not row['thinking_closed']:
            assert not (folder/'answer.md').read_text(encoding='utf-8')
            assert not (folder/'test_candidate.py').exists()
result=dict(passed=True,cells=6,checks=['Unique predeclared task/model cells','Identical rendered prompts and lengths within each task','Stored input and model fingerprints unchanged','Token counts and predeclared budget','No prompt truncation','Thinking closure and final-answer extraction','Termination versus truncation'],final_test_access='None in evaluation scripts; only two explicit development tasks.')
(out/'consistency_checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
