"""Create human-readable review material only from a passed, hash-bound candidate."""
import argparse, collections, hashlib, json, pathlib
ROOT=pathlib.Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--dataset",required=True); p.add_argument("--validation",required=True)
    p.add_argument("--profile",required=True); p.add_argument("--audit",required=True)
    a=p.parse_args()
    dataset=ROOT/a.dataset
    manifest=json.loads((dataset/"manifest.json").read_text(encoding="utf-8"))
    validation=json.loads((ROOT/a.validation/"summary.json").read_text(encoding="utf-8"))
    profile=json.loads((ROOT/a.profile).read_text(encoding="utf-8"))
    audit=json.loads((ROOT/a.audit).read_text(encoding="utf-8"))
    fingerprint=hashlib.sha256((dataset/"SHA256.json").read_bytes()).hexdigest()
    assert validation["status"]==audit["status"]=="passed"
    assert all(x["dataset_hash_manifest_sha256"]==fingerprint for x in [validation,profile,audit])
    records=manifest["tasks"]; lengths={r["id"]:r["tokens"] for r in profile["rows"]}
    counts=collections.Counter(r["split"] for r in records)
    families={s:len({r["family"] for r in records if r["split"]==s}) for s in counts}
    text=f"""# Qwenny dataset v1 — assembled, independent review pending

Current candidate: **{a.dataset}**. Earlier candidate folders are retained assembly
drafts; use this one for review. No model has been trained on this corpus.

| Split | Tasks | Declared families |
|---|---:|---:|
"""+''.join(f"| {s} | {counts[s]} | {families[s]} |\n" for s in ["training","development","final","regression"])+f"""
The 60 training tasks ask for pytest suites from precise function contracts.
Development and final tasks use the same task type. Regression includes four
implementation tasks, four repairs and four explanations. All content was
originally authored for this project; no external dataset or failed Qwen answer
was used. Previously exposed batches/prefix-removal families stay in training;
rotation/clock parsing stay in development.

Automated evidence for this exact candidate:

- {validation['reference_suites']} executable reference suites passed, with {validation['reference_test_cases']} pytest cases.
- All {validation['designated_mutants']} designated single-defect mutants failed at a recorded result/post-state assertion or required-exception witness.
- Four original regression bugs reproduced; these are separate from mutant scores.
- Four explanation snippets reproduced their expected values; rubric scoring still needs a person.
- {manifest['oracle_valid_input_checks']:,} valid-input checks against separate oracle methods passed.
- No declared family ID crosses splits, and no exact normalized reference-source clone crosses splits.
- No evaluator answers occur as assistant messages in development/final/regression model packets.

These checks are all same-author/agent evidence. They do not establish independent
review, exhaustive correctness, semantic family independence or statistical power.
Some mutants are simple type/boundary/cardinality defects; detection is not a
general quality score. Broader behavior and equivalent/invalid-mutant judgments
remain review work. General pretrained contamination cannot be excluded.

## Review and evidence

- [Training review table](REVIEW_TRAINING.md)
- [Review guide](REVIEW_GUIDE.md)
- [All 108 task records]({a.dataset}/INDEX.md)
- [Automated validation]({a.validation}/summary.json)
- [Token profile]({a.profile})
- [Mechanical split/source audit]({a.audit})
- [Draft approvals file]({a.dataset}/approvals.template.json)

Each task contains its contract, target, source record, separate reference/oracle,
explicit cases and three mutant witnesses. Evaluator files are separate from model
messages. References/oracles/mutants and final answers must not enter trainer input.
Automated results are in the separate hash-bound validation report; authoring-time
placeholders inside the snapshot are not the current validation result.

## Local length and training boundary

All 60 complete training chats total **{profile['total_tokens']:,} tokens** under the
explicit thinking-disabled profiling setting: minimum {profile['minimum']}, median
{profile['median']:g}, 90th percentile {profile['p90_nearest_rank']}, maximum
**{profile['maximum']}**. Nothing was truncated. Token lengths depend on the final
chat/reasoning policy; that policy is not approved by this profile.

The longest example exceeds the 768-token GPU benchmark. Before task training,
measure the complete maximum-length example (approximately 2048-token capacity)
on the local 3080 with the chosen loss/masking path. The earlier 15–30 minute
planning allowance is not a new full-dataset runtime measurement.

No app shutdown is required for CPU-only assembly. Recheck dedicated/shared GPU
memory before the next GPU trial; do not close Claude, Edge or other apps automatically.

## Approval/export boundary

The candidate is not frozen or approved for training. export_reviewed.py requires
a passed exact-content validation, an independent family/split audit and explicit
per-training-record approvals tied to reference/spec/target/answer hashes.
The empty approval template must not be bulk-approved from test counts.
Export also does not select reasoning policy or validate assistant-only loss masks;
those are separate pre-training checks.

Candidate hash-manifest SHA256: {fingerprint}.
"""
    (ROOT/"README.md").write_text(text,encoding="utf-8")
    guide="""# Independent review guide

The assembly task is complete; this guide is the quality gate before training.
Your earlier review of feasibility results did not approve these newly authored
examples. Project 03_DATASET_RULES.md calls for reviewed successful targets and a
family-level split, so independent review is recorded separately from automated checks.

For each training row, read SPEC.md and TARGET.md together. Trace every explicit
argument tuple, result and exception. Check exact built-in types (including bool
and subclass rejection), value/type precedence, empty/boundary cases, and any
mutation/identity rule. Verify that the target imports only the stated function
and does not implement or inspect it. Check the brief mapping and limitations.

Then examine the separate oracle method and each mutant's concrete witness.
Check that the reference agrees with the written contract, that rejection cases
are intentional, and that mutants are genuine single defects rather than equivalent
implementations. Passing one reference alone is not sufficient. Bounded oracle
checks and generated cases are not an independent person's review.

Audit function/problem-family similarity across all four splits. The automated
check removes names/literal values and looks for exact structural clones; it cannot
certify semantic novelty. A renamed or constant-changed variant must remain with
its family. Existing rotation/clock development tasks and earlier visible tasks
cannot be presented as unseen final tests.

Record a real reviewer identity, exact hashes, decision and concrete notes in a
copy of approvals.template.json. Do not overwrite the candidate snapshot or forge
a reviewer/approval. Fixes require a new candidate and validation of changed content.
The export guard requires all 60 training records and the family audit to be approved.
Final/development/regression target reviews remain necessary before formal scoring.

Before training, pin the reasoning/direct-answer policy, verify assistant-only
masking and nonzero target tokens, fit full examples without truncation, and repeat
matched base A/B controls in the eventual runtime. Only then compare an adapter.
"""
    (ROOT/"REVIEW_GUIDE.md").write_text(guide,encoding="utf-8")
    table="# Training candidate review table\n\nAll decisions are pending independent review. Token counts include the full provisional chat format.\n\n| ID | Function | Family | Tokens | Reference cases | Type-before-value witnesses | Review files |\n|---|---|---|---:|---:|---:|---|\n"
    for r in records:
        if r["split"]!="training": continue
        base=f"{a.dataset}/tasks/training/{r['id']}"
        table+=f"| {r['id']} | {r['function']} | {r['family']} | {lengths[r['id']]} | {r['valid_test_cases']+r['exception_test_cases']} | {r['type_before_value_witnesses']} | [Contract]({base}/SPEC.md), [Target]({base}/TARGET.md), [Witnesses]({base}/evaluator/mutants.json), [Review]({base}/REVIEW.md) |\n"
    (ROOT/"REVIEW_TRAINING.md").write_text(table,encoding="utf-8")
    (ROOT/"CURRENT_CANDIDATE.txt").write_text(a.dataset+"\n",encoding="utf-8")
    print("Review documentation written for",a.dataset)

if __name__=="__main__": main()
