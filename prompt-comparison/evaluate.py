"""Run a saved candidate in isolated fixture folders; review detections manually.

Usage: python evaluate.py T01 path/to/test_candidate.py path/to/new/result-folder
Generated code executes with the interpreter's normal permissions. Inspect it first.
"""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
from build_materials import ROOT, write

p=argparse.ArgumentParser()
p.add_argument('task',choices=['T01','T02'])
p.add_argument('candidate',type=Path)
p.add_argument('output',type=Path)
a=p.parse_args()
if a.output.exists():
    p.error('Choose a new output folder to preserve earlier attempt evidence.')
task=ROOT/'evaluation'/a.task
meta=json.loads((task/'metadata.json').read_text(encoding='utf-8'))
results={}
for fixture in sorted((task/'fixtures').iterdir(),key=lambda f:f.name!='reference'):
    target=a.output/fixture.name
    target.mkdir(parents=True)
    shutil.copyfile(a.candidate,target/'test_candidate.py')
    shutil.copyfile(fixture/(meta['module']+'.py'),target/(meta['module']+'.py'))
    try:
        run=subprocess.run([sys.executable,'-m','pytest','-q','-p','no:cacheprovider','test_candidate.py'],cwd=target,capture_output=True,text=True,timeout=30)
        log=run.stdout+run.stderr
        code=run.returncode
    except subprocess.TimeoutExpired:
        log='TIMEOUT: no valid detection credited'
        code='timeout'
    write(target/'pytest.log',log)
    results[fixture.name]={'exit_code':code,'assertion_failure_candidate':code==1 and 'FAILED test_candidate.py::' in log and 'ERROR collecting' not in log}
valid=results['reference']['exit_code']==0
write(a.output/'execution_summary.json',json.dumps({'task':a.task,'reference_valid':valid,'mutant_score_eligible':valid,'results':results,'acceptance':'PENDING manual category, relevant failure, code and prose review'},indent=2))
write(a.output/'REVIEW.md','''# Attempt review

Arm: A / B
Seed: 42
Attempt: first / repair-01
Exact full request and response saved: pending
Effective settings/model identity checked: pending
Completion and context overflow: pending
Required categories and concrete witnesses: pending
Relevant mutant detections (exclude imports, crashes, timeouts): pending
Unsupported execution/completeness claims: pending
Generation time, tokens and operator effort: pending
Task acceptance: pending

Record the first attempt before feedback. Save one repair in a new folder.
''')
print(json.dumps({'reference_valid':valid,'results':results},indent=2))
