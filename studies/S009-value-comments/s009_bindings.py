"""Strict frozen study/export guards; no legacy default corpus selection."""
from prepare_study import HERE,EXP,read,sha
def verify_variant(folder,approved_hash):
    report=read(folder/'report.json')
    assert approved_hash and sha(folder/'messages.jsonl')==approved_hash==report['messages_jsonl_sha256'],'Unapproved exact packet hash'
    for name in ('train','development'):
        assert sha(folder/(name+'.jsonl'))==report[name+'_jsonl_sha256'],('Changed prepared data',name)
    return report

def verify_prepared(path):
    path=path.resolve(); prep=HERE/'preparation-001'
    assert path in [(prep/a).resolve() for a in ('baseline','comments')],'Unbound prepared corpus'
    auth=read(prep/'authorization.json')
    return verify_variant(path,auth['approved_export_hashes'][path.name])
def verify_frozen():
    frozen=read(HERE/'freeze-manifest.json')
    for name,expected in frozen['files'].items():
        assert sha(EXP/name)==expected,('Frozen source changed',name)
    for gate in ('validation-001','scorer-calibration-001'):
        assert read(HERE/gate/'summary.json')['status']=='passed',gate
    prep=HERE/'preparation-001'; auth=read(prep/'authorization.json')
    for arm in ('baseline','comments'):
        verify_variant(prep/arm,auth['approved_export_hashes'][arm])
    return frozen
