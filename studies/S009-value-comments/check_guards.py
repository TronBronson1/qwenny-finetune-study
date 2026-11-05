"""Exercise positive authorization and concrete wrong-hash/changed-file rejection."""
import pathlib,shutil,tempfile
from prepare_study import HERE,read,dump,sha
from s009_bindings import verify_variant,verify_prepared
def rejects(fn):
    try: fn()
    except AssertionError: return True
    return False
def main():
    prep=HERE/'preparation-001'; auth=read(prep/'authorization.json'); checks={}
    for arm in ('baseline','comments'):
        verify_variant(prep/arm,auth['approved_export_hashes'][arm]); checks[arm+'-approved']=True
        checks[arm+'-wrong-hash']=rejects(lambda:verify_variant(prep/arm,'0'*64))
        checks[arm+'-missing-approval']=rejects(lambda:verify_variant(prep/arm,None))
    with tempfile.TemporaryDirectory(prefix='s009-guard-',dir=HERE) as temp:
        folder=pathlib.Path(temp)/'variant'; shutil.copytree(prep/'baseline',folder)
        with (folder/'train.jsonl').open('a',encoding='utf-8') as f:f.write('\n')
        checks['changed-prepared-rejected']=rejects(lambda:verify_variant(folder,auth['approved_export_hashes']['baseline']))
    checks['legacy-prepared-rejected']=rejects(lambda:verify_prepared(HERE.parents[1]/'training-v1/prepared-001'))
    dump(HERE/'guard-checks.json',dict(status='passed' if all(checks.values()) else 'failed',checks=checks,script_sha256=sha(pathlib.Path(__file__))))
    assert all(checks.values())
if __name__=='__main__':main()
