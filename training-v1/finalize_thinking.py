"""Finalize the matched thinking control without modifying prior experiments."""
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
probe=ROOT/'probes/thinking-001'
score=ROOT/'scoring/thinking-001-pytest'
report=json.loads((probe/'report.json').read_text())
execution=json.loads((score/'summary.json').read_text())
assert report['status']=='completed' and len(report['completed'])==6
assert json.loads((probe/'consistency_checks.json').read_text())['passed']
scores={(r['task'],r['variant']):r for r in execution['results']}
reasons={
 ('DV001','base'):'Truncated after a complete code block; 24 reference tests fail because supposed valid/nonmutation inputs are lists, not exact tuples. Additional wrong negative-rotation and identity expectations; mapping truncated.',
 ('DV001','original-e5'):'Complete response, but collection fails with NameError: nested is undefined. Additional flattened argument/expected parametrization, invalid exception classes and identity assertions.',
 ('DV001','compact-e5'):'All 8192 tokens consumed before closing the thinking section. No final answer or candidate file.',
 ('DV002','original-e5'):'All 8192 tokens consumed before closing the thinking section. No final answer or candidate file.',
 ('DV002','compact-e5'):'All 8192 tokens consumed before closing the thinking section. No final answer or candidate file.',
 ('DV002','base'):'Thinking closes, but the final code truncates at an unfinished assignment with no closing fence or mapping. Visible code also expects TypeError for malformed exact strings, which require ValueError.',
}
rows=[]
for gen in report['completed']:
    key=(gen['task'],gen['variant']); result=scores[key]
    assert not result['provisional_executable_pass']
    if result['execution']=='completed':
        assert not result['reference_valid']
        assert result['variants']['reference']['test_cases']>0
    folder=probe/gen['task']/gen['variant']
    rows.append(dict(**gen, execution=result['execution'], reference_valid=result.get('reference_valid'), eligible_mutant_kills=result.get('eligible_mutant_kills'), strict_accepted=False, reason=reasons[key], answer_sha256=hashlib.sha256((folder/'answer.md').read_bytes()).hexdigest(), review_basis='Definitive truncation, missing-final-answer or reference/collection failure. Additional visible defects noted; no repaired output or exhaustive coverage claim.'))
review=dict(scope='Matched thinking-enabled development control, seed42, cap8192 total reasoning+answer. No final-test evaluation.', rows=rows)
(score/'agent-acceptance-review.json').write_text(json.dumps(review,indent=2),encoding='utf-8')
gpu=[]
for line in (probe/'gpu-memory.csv').read_text().splitlines()[1:]:
    parts=line.split(',')
    if len(parts)==4:
        try: gpu.append(tuple(float(v.strip()) for v in parts))
        except ValueError: pass
summary=dict(status='completed', scope=review['scope'], models=['base','original-e5','compact-e5'], tasks=['DV001','DV002'], settings={k:report[k] for k in ('thinking','seed','temperature','top_k','top_p','presence_penalty','repetition_penalty','max_new_tokens','context_limit')}, reload_checks=report['reload_checks'], strict_accepted_by_model={v:sum(r['strict_accepted'] for r in rows if r['variant']==v) for v in ('base','original-e5','compact-e5')}, tasks_per_model=2, terminated=sum(r['terminated'] for r in rows), truncated=sum(r['truncated'] for r in rows), thinking_never_closed=sum(not r['thinking_closed'] for r in rows), complete_final_python_blocks=sum(r['python_blocks']==1 for r in rows), generated_tokens=sum(r['generated_tokens'] for r in rows), generation_seconds=sum(r['seconds'] for r in rows), peak_torch_allocated_bytes=max(r['memory']['peak_allocated'] for r in rows), peak_torch_reserved_bytes=max(r['memory']['peak_reserved'] for r in rows), sampled_gpu_min_free_MiB=min(r[2] for r in gpu), windows_process_memory='Unavailable: CSV has header only; no claim about per-process shared-memory spill.', scoring='scoring/thinking-001-pytest/summary.json', scoring_scope_note='Unchanged legacy evaluator summary says direct-answer pilot; this wrapper and the generation plan identify the actual thinking-enabled configuration.', infrastructure_failure='scoring/thinking-001 used training Python without pytest. Its logs/summary are preserved and excluded from all model-quality evidence. Same immutable generated files were then scored with the established Python3.15 pytest9.2 interpreter; no inference retry.', rows=rows, interpretation='No accepted answer in this bounded two-family/one-seed control. This does not rank general aptitude, prove a quantization cause, or replicate unrestricted presence1.5 GGUF/LM Studio history. No candidate selected; no further training performed.', final_test='Untouched; scripts reference only two development tasks. No failed development output used as training data.')
(ROOT/'thinking-control-results.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
lines=['# Thinking-enabled control 001 results — 2026-11-04','',
'Completed locally on the RTX 3080. Base, original E5 and compact E5 each scored **0/2 strict accepted**. No candidate selected. Existing models and prior experiment results were preserved; final and regression tasks remain untouched.','',
'## Matched protocol','',
'Pinned Qwen3.5-9B revision c202236235762e1c871ad0ccb60c8ee5ba337b9a, existing NF4/BF16 CPU-embedding runtime. Both E5 adapters reproduced saved probe logits exactly (max abs difference 0). Only the already-visible DV001 rotation and DV002 clock instruction-only messages were used. Rendered prompts and token counts matched within each task.','',
'Thinking on; seed42 reset per cell; temperature1/top_k20/top_p.95; presence0/repetition1; 8192 total new tokens shared by reasoning and answer, context ceiling16134, explicit im_end/endoftext stops. One first attempt per cell. No prompt truncation, repairs, inference retries, best-of-N or cap increase. Protocol was saved before generation in THINKING_CONTROL_PLAN.md.','',
'This is a bounded Python-runtime control, not historical unrestricted LM Studio GGUF with presence1.5. Comparisons with old thinking-off cap2048 results change both thinking and budget and cannot isolate thinking alone.','',
'## All first attempts','',
'| Task | Model | Total tokens | Before thinking close | After close | Terminated | Final block | Strict accepted |',
'|---|---|---:|---:|---:|---|---|---|']
for row in rows:
    before=str(row['reasoning_tokens_before_close']) if row['thinking_closed'] else 'no close'
    lines.append(f"| {row['task']} | {row['variant']} | {row['generated_tokens']} | {before} | {row['final_tokens_after_close']} | {'Yes' if row['terminated'] else 'No, cap'} | {'Yes' if row['python_blocks']==1 else 'No'} | No |")
lines += ['', 'Counts after the closing delimiter include any final stop token. Reasoning never closed in three cells; those cells have zero final-answer tokens, not zero reasoning tokens. Five of six responses hit the cap. The only terminated response was original E5 rotation, which failed collection.', '', '## Execution and review','',
'Every complete final candidate was read and hash-bound before unchanged isolated reference/three-mutant pytest execution. Reasoning code was never extracted as a final answer. Both executable candidate files failed the correct reference, so neither is eligible for mutant-detection credit. No incomplete code was repaired or executed.','']
for row in rows: lines.append(f"- **{row['task']} / {row['variant']}:** {row['reason']}")
lines += ['', 'The initial scoring launch mistakenly used the model environment, which lacks pytest. Those infrastructure logs remain under scoring/thinking-001 and are excluded from quality evidence. The same saved candidates were then scored with the established Python3.15 / pytest9.2 interpreter under scoring/thinking-001-pytest. No generated answer changed. The unchanged evaluator retains a generic direct-answer scope string; the plan, generation report and this report specify the actual thinking-enabled run.', '', '## Runtime and evidence','',
f"Six generations produced {summary['generated_tokens']:,} tokens and took {summary['generation_seconds']:.3f} seconds ({summary['generation_seconds']/60:.1f} minutes), excluding loading, base verification, probe checks and scoring. The first base rotation generation was unusually slow. Timings include local runtime/memory conditions and do not isolate adapter effects.", '',
f"Torch peak allocated {summary['peak_torch_allocated_bytes']/1024**3:.2f} GiB / reserved {summary['peak_torch_reserved_bytes']/1024**3:.2f} GiB. GPU-wide sampled minimum free memory was {summary['sampled_gpu_min_free_MiB']:.0f} MiB. Windows per-process memory counters produced no samples; shared-memory spill is unverified. No OOM was reported. The generation process exited successfully and its temporary keep-awake request ended.", '',
'- probes/thinking-001/: raw outputs, token IDs, final answer extraction, exact prompts, hashes, reload/consistency checks, timing and GPU logs.',
'- scoring/thinking-001-pytest/: definitive unchanged execution logs and agent-acceptance-review.json.',
'- thinking-control-results.json: complete machine-readable comparison.',
'- thinking-control-sha256.json: artifact fingerprints.', '', '## Interpretation','',
'Thinking enabled did not produce an accepted answer in this bounded control. Long repetitive reasoning consumed most or all of the budget, while the two complete final files remained contract-invalid. This does not prove that a larger budget would help, that training universally helps/harms, that 4-bit precision caused the failures, or that historical LM Studio behavior is reproduced. Two visible families and one seed cannot rank general aptitude.', '',
'Retain all candidates without adopting a winner. Freeze any next development protocol separately. Do not increase this run\'s cap, rescue these outputs, use failed development outputs as targets, or open final-test families to choose a candidate. No optimizer updates, cloud work, GGUF conversion or LM Studio changes occurred.']
(ROOT/'THINKING_CONTROL_RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(ROOT/'scoring/thinking-001/INFRASTRUCTURE_FAILURE.md').write_text('This scoring launch used the training Python, which has no pytest. All execution logs report No module named pytest. Do not use its summary for model-quality claims. Unchanged saved outputs were scored with the established pytest interpreter under ../thinking-001-pytest. No generation was repeated.\n',encoding='utf-8')
handoff='''# Qwenny handoff — matched thinking control complete

2026-11-04 America/New_York. Read training-v1/THINKING_CONTROL_RESULTS.md next.
Prior base/environment/training authorization and compact trial details remain
in HANDOFF_TRAINED_QWENNYS.md and HANDOFF_COMPACT_TRIAL.md.

Matched pinned NF4 base / original E5 / compact E5 on already-visible development
DV001/DV002, instruction-only. Thinking enabled, seed42, temp1/topk20/topp.95,
presence0/repetition1, cap8192 shared reasoning+answer, context16134, explicit stops.
Both E5 import probes exact (max abs0); prompt matching/input hashes verified.

All three models 0/2 strict accepted. Five of six hit cap. Compact both tasks and
original E5 clock never closed thinking/no final answer. Base rotation produced
a complete fence but wrong list inputs (24 reference failures), mapping truncated.
Original E5 rotation terminated at6904 tokens, but undefined nested causes
collection failure. Base clock closed thinking then truncated inside code/no fence.
No repairs, retries, cap increase, best-of-N, or failed-output training targets.

Full first attempts: training-v1/probes/thinking-001. Definitive unchanged execution:
training-v1/scoring/thinking-001-pytest. Initial scoring/thinking-001 used training
Python without pytest; preserved as infrastructure failure, excluded from quality
claims. Same outputs then executed with established Python3.15/pytest9.2.
thinking-control-results.json links final machine results; hashes preserved.

This is bounded Python thinking-on presence0, NOT historical unrestricted GGUF
LM Studio presence1.5. Old direct-answer2048 comparisons confound mode/budget.
Two visible families/one seed cannot rank aptitude or justify quantization blame.
No winner selected and no additional training performed. Keep final/regression
tasks untouched until candidate and final protocol are frozen. Any next development
configuration must be separately predeclared, never a rescue of these attempts.

Generation and scoring jobs exited. Temporary process keep-awake ended. Existing
models/results preserved; no cloud, app closure, LM Studio changes, merge or export.
GPU-wide logs available; Windows per-process shared-memory samples unavailable.
'''
(ROOT.parent/'HANDOFF_THINKING_CONTROL.md').write_text(handoff,encoding='utf-8')
paths=[ROOT/'THINKING_CONTROL_PLAN.md',ROOT/'THINKING_CONTROL_RESULTS.md',ROOT/'thinking-control-results.json',ROOT/'thinking_probe.py',ROOT/'verify_thinking.py',ROOT/'finalize_thinking.py',ROOT.parent/'HANDOFF_THINKING_CONTROL.md']
paths += [p for folder in (probe,score,ROOT/'scoring/thinking-001') for p in folder.rglob('*') if p.is_file()]
hashes={str(p.relative_to(ROOT.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
(ROOT/'thinking-control-sha256.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k not in ('rows','reload_checks')},indent=2))
