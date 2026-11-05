"""Bind training, import and first-attempt pilot evidence into a readable local report."""
import hashlib,json,pathlib,xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).resolve().parent
def main():
    run=ROOT/"runs/qwenny-001"
    trained=json.loads((run/"report.json").read_text()); assert trained["status"]=="trained"
    probe=ROOT/"probes/qwenny-001-direct-001"; generated=json.loads((probe/"report.json").read_text()); assert generated["status"]=="completed"
    scoring=ROOT/"scoring/qwenny-001-direct-001"; scored=json.loads((scoring/"summary.json").read_text())
    cache=json.loads((ROOT/"diagnostics/qwenny-001-cache-001/report.json").read_text()); assert cache["status"]=="completed"
    gap=json.loads((ROOT/"diagnostics/qwenny-001-exact-int-gap/report.json").read_text())
    assert gap["results"]["model"]["exit_code"]==0 and gap["results"]["gold"]["exit_code"]==1
    reviews=json.loads((probe/"code_inspections.json").read_text())
    findings={
        ("DV001","base-A"):"Reference-invalid: incorrect expected negative, nested and oversized rotations.",
        ("DV001","base-B"):"Collection failure: missing pytest import; additional invalid cases do not repair it.",
        ("DV001","epoch-1-C"):"Collection failure: parametrization includes error_message but function signature omits it.",
        ("DV001","epoch-3-C"):"Incomplete at 2048-token cap; no complete Python code block.",
        ("DV001","epoch-5-C"):"Syntax-invalid code, including malformed parametrization and English pseudo-code.",
        ("DV002","base-A"):"Reference-invalid: malformed builtin string incorrectly expects TypeError; further type/Unicode coverage gaps.",
        ("DV002","base-B"):"Collection failure: missing pytest import and inconsistent dynamic subclass name/signature.",
        ("DV002","epoch-1-C"):"Reference-valid and 3/3 designated mutants detected, but exact built-in int coverage is missing. A non-bool int-subclass diagnostic passes all 24 model tests, while the gold suite detects it.",
        ("DV002","epoch-3-C"):"Collection failure: malformed parametrize decorator. Only one valid case, inexact output check and unsupported exception-message constraint.",
        ("DV002","epoch-5-C"):"Reference-invalid: malformed strings assigned wrong exception type, valid midnight expected to fail, and wrong function arity."}
    rows=[]
    for item in scored["results"]:
        key=(item["task"],item["variant"])
        rows.append({**{k:item.get(k) for k in ["task","variant","reference_valid","eligible_mutant_kills","provisional_executable_pass","truncated"]},
                     "agent_strict_acceptance":False,"reason":findings[key],"review_basis":"Execution/termination failure, or the demonstrated explicit exact-output-type coverage gap. This does not assert a complete review of every prose/category issue."})
    assert len(rows)==10
    write=lambda path,obj:path.write_text(json.dumps(obj,indent=2),encoding="utf-8")
    write(scoring/"agent-acceptance-review.json",{"scope":"Two visible development families, one seed, bounded direct-answer pilot. No repairs or cherry-picked samples.","posthoc_exact_type_diagnostic_excluded_from_frozen_mutant_score":True,"rows":rows})
    table=[]
    for variant in ["base-A","base-B","epoch-1-C","epoch-3-C","epoch-5-C"]:
        items=[r for r in rows if r["variant"]==variant]
        table.append({"variant":variant,"tasks":2,"reference_valid_suites":sum(r["reference_valid"] is True for r in items),"provisional_executable_passes":sum(r["provisional_executable_pass"] is True for r in items),"agent_strict_acceptance":sum(r["agent_strict_acceptance"] for r in items),"incomplete":sum(r["truncated"] for r in items)})
    summary={"training":"completed","candidates":["Qwenny-E1","Qwenny-E3","Qwenny-E5"],"fresh_import_checks":generated["reload_checks"],"pilot":table,"quality_conclusion":"No strict-acceptance advantage demonstrated in this two-family one-seed bounded direct-answer pilot. Do not treat lower teacher-forced loss as proof of useful aptitude. Thinking-enabled historical settings, broader regression and final-test scoring remain untested.","cache_diagnostic":[{"variant":r["variant"],"checked_positions":len(r["rows"]),"argmax_matches":sum(x["argmax_matches"] for x in r["rows"]),"max_kl":max(x["kl_full_to_cached"] for x in r["rows"]),"max_abs_logit_difference":max(x["max_abs_difference"] for x in r["rows"])} for r in cache["results"]]}
    write(ROOT/"RESULTS.json",summary)
    text="""# Qwenny training v1 — trained and import-verified; quality gain not demonstrated

Three experimental adapters are saved: **Qwenny E1, E3 and E5**, after 1, 3 and 5
passes through the same 60-task corpus. They are checkpoints on one trajectory,
not independently trained models or verified tiers of aptitude. All three loaded
into a fresh base and reproduced stored probe logits exactly.

## Artifacts

- [Qwenny E1](candidates/qwenny-001/Qwenny-E1/README.md)
- [Qwenny E3](candidates/qwenny-001/Qwenny-E3/README.md)
- [Qwenny E5](candidates/qwenny-001/Qwenny-E5/README.md)
- [Training settings and scope](PLAN.md)
- [Training report](runs/qwenny-001/report.json)
- [Complete first-attempt generation records](probes/qwenny-001-direct-001/report.json)
- [Execution score](scoring/qwenny-001-direct-001/summary.json)
- [Agent acceptance review](scoring/qwenny-001-direct-001/agent-acceptance-review.json)
- [Exact-output-type diagnostic](diagnostics/qwenny-001-exact-int-gap/report.json)
- [Cached/full-forward diagnostic](diagnostics/qwenny-001-cache-001/report.json)

Each candidate has the exact adapter_config.json and adapter_model.safetensors
copies, SHA256 fingerprints and provenance. The adapter weight file is 2232928
bytes. Base weights remain separate and unchanged on disk. The pinned base is
Qwen/Qwen3.5-9B at c202236235762e1c871ad0ccb60c8ee5ba337b9a.

## Training and loss

The local run completed 300 training microbatches / 75 optimizer updates, with
every training task used exactly five times. It took about 11.6 minutes from the
start of optimizer training through checkpoint development-loss checks; loading,
preflight, base controls and generation scoring are extra. Median training
microbatch time was 2.0 seconds. No base parameters received gradients, intended
adapter gradients were finite/nonzero, and every optimizer update changed them.

Assistant-only tokenization was checked on every example. Full answers and im_end
were supervised; prompts/roles/empty thinking wrapper were ignored. Nothing was
truncated. The actual longest example completed backward before optimizer training,
and cached generation terminated correctly in the smoke check.

| Weights | Instruction-only prompt loss | With fixed demonstrations loss |
|---|---:|---:|
| Base (A/B) | 0.8934 | 0.7899 |
| E1 (C/optional D) | 0.7698 | 0.7082 |
| E3 (C/optional D) | 0.3816 | 0.4306 |
| E5 (C/optional D) | 0.1329 | 0.2218 |

These are mean per-example teacher-forced assistant-token losses on the 12
development targets. The labels/answers were never optimizer training data.
Likelihood improved, but the free-running results below show why it is not a
substitute for executable acceptance or reasoning/regression evaluation.

Training-stage allocator peaks were about 7.07 GiB allocated / 7.57 GiB reserved.
CUDA-reported free memory reached about 414 MiB at a recorded microbatch stage;
Windows process shared usage peaked at 82 MiB over the training interval. All
300 microbatches completed without reported OOM/nonfinite-gradient failure, but
headroom is still limited and desktop occupancy can vary.

## First-attempt generation pilot

This is a **separate bounded direct-answer pilot**, not the historical thinking-on
LM Studio comparison: thinking disabled, seed 42, temperature 1, top_k 20,
top_p .95, output-only presence penalty 1.5, maximum 2048 new tokens. The penalty
implementation is recorded and is not claimed identical to LM Studio's. Exactly
one answer per task/variant was saved; no repairs, retries or best-of-N selection.
The tasks were the already-visible development rotation and clock families.

| Variant | Reference-valid suites | Reference + 3 mutants + complete format | Agent strict acceptance |
|---|---:|---:|---:|
"""+''.join(f"| {r['variant']} | {r['reference_valid_suites']}/2 | {r['provisional_executable_passes']}/2 | {r['agent_strict_acceptance']}/2 |\n" for r in table)+"""
The only provisional executable success was E1 on clock parsing. It still used
isinstance(result,int), allowing non-bool int subclasses. A separate post-hoc
diagnostic implementation returns such a subclass: all 24 generated tests pass,
while the gold suite detects it. This diagnostic validates a pre-existing explicit
requirement; it is not added to the frozen three-mutant denominator.

Other answers had collection errors, incorrect expected values/exceptions, wrong
arity or syntax errors. E3's rotation answer hit the cap without closing its code
block. Cutoff responses and reference-invalid suites were not credited with mutant
scores. All complete code blocks were read and hash-bound source inspection was
recorded before isolated execution. Original answers were never repaired or altered.

Two task families and one seed are insufficient to rank general aptitude. The
zero strict passes show no acceptance gain in this pilot; they do not prove
training is universally harmful, establish that quantization caused the errors,
or measure behavior under thinking-enabled inference. The 24 final tasks and
broader regression set have not been evaluated by these models.

## Cache and deployment compatibility

Fresh adapter import is verified. A read-only cache diagnostic compared raw cached
decoding logits with full-context forwards on five positions from each of base
and E5. Top-token choices matched 5/5 for both; maximum KL was about 0.00190 and
0.00123 respectively. Raw logits were not bit-identical (largest absolute
differences 0.5625/0.75). This bounded result showed no gross mismatch at those
positions; it does not rule out all long-sequence/cache/numerical issues.

These are PEFT adapters, **not standalone LM Studio GGUF models**. The documented
LM Studio import route takes model files such as GGUF. Merge/conversion and matched
requantized base/adapted validation remain a separate stage. No working LM Studio
model/settings were replaced and no cloud rental or upload was started.

## Decision

Retain all three experimental candidates and the working base. Do not adopt a
checkpoint on the loss table alone. Next investigate the gap between target
likelihood and free-running correctness with properly matched thinking-enabled/
decoding controls and simpler target-format ablations on development data before
further training. Keep final-test families untouched until a candidate/protocol is
frozen. No general coding or reasoning improvement is claimed.
"""
    (ROOT/"README.md").write_text(text,encoding="utf-8")
    write(ROOT/"candidates/qwenny-001/PILOT_RESULTS.json",summary)
    for epoch in (1,3,5):
        folder=ROOT/"candidates/qwenny-001"/f"Qwenny-E{epoch}"
        metadata=json.loads((folder/"EXPERIMENT.json").read_text())
        metadata["bounded_direct_answer_pilot"]=next(r for r in table if r["variant"]==f"epoch-{epoch}-C")
        metadata["quality_claim"]="No strict acceptance gain demonstrated in the two-family pilot; not an adopted model."
        write(folder/"EXPERIMENT.json",metadata)
        for name,digest in metadata["files"].items(): assert hashlib.sha256((folder/name).read_bytes()).hexdigest()==digest
    print(json.dumps(summary,indent=2))

if __name__=="__main__": main()
