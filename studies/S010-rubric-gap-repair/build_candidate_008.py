"""CPU-only candidate-008 builder: candidate-007 plus declared gap repairs.

    python3 studies/S010-rubric-gap-repair/build_candidate_008.py --reproduce-007   # equivalence check only
    python3 studies/S010-rubric-gap-repair/build_candidate_008.py                   # writes dataset-v1/candidate-008

Reuses candidate-007's own builder functions (dataset-v1/candidate-007/build-sources/build_repair.py)
so generation is identical; --reproduce-007 regenerates candidate-007's code/case/prompt files in a
temporary directory and requires byte equality before anything is written. Imports training and
development definitions only; final/regression tasks are never read. Refuses to overwrite.
"""
import sys
sys.dont_write_bytecode = True
import argparse, copy, hashlib, importlib.util, json, pathlib, shutil, tempfile

HERE = pathlib.Path(__file__).resolve().parent
EXP = HERE.parents[1]
DATA = EXP / "dataset-v1"
C6, C7, C8 = DATA / "candidate-006", DATA / "candidate-007", DATA / "candidate-008"
AUDIT = EXP / "independent-review" / "c007-rubric-audit"

spec = importlib.util.spec_from_file_location("build_repair_007", EXP / "studies" / "S007-measurement-repair" / "build_repair.py")
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)          # executes 007's helper setup (candidate-006 build-sources only)
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(AUDIT))
import repair_config_008 as R8      # noqa: E402
import mutants_lib                  # noqa: E402  (independent audit mutant families)
import probes                       # noqa: E402

ns = B.ns


def sha_text(text):
    return hashlib.sha256(text.encode()).hexdigest()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assemble_task(split, original, additions):
    """Mirror of candidate-007 main() per-task assembly, with optional 008 additions."""
    record = json.loads((original / "record.json").read_text(encoding="utf-8"))
    ident = record["id"]
    task = copy.deepcopy(B.tasklib.TASKS[record["function"]])
    reference = (original / "evaluator/reference/subject.py").read_text(encoding="utf-8")
    assert reference == B.tasklib.source(task), (ident, "reference/source mismatch")
    labels = B.LABELS[ident].split("|")
    assert len(labels) == len(task.inputs)
    valid_add = list(B.VALID.get(ident, [])) + (R8.VALID_008.get(ident, []) if additions else [])
    invalid_add = list(B.INVALID.get(ident, [])) + (R8.INVALID_008.get(ident, []) if additions else [])
    for args, label in valid_add:
        task.inputs.append(args); labels.append(label)
    task.invalid.extend((args, error) for args, error, label in invalid_add)
    if "tuple3" in task.schemas:
        for position, schema in enumerate(task.schemas):
            if schema != "tuple3":
                continue
            for component in range(3):
                args = list(copy.deepcopy(task.inputs[0])); row = [0, 0, 0]; row[component] = -1
                args[position] = tuple(row); task.invalid.append((tuple(args), "ValueError"))
    fn = ns["compile_function"](reference, task.name)
    valid, invalid, checks = ns["build_cases"](task, fn)
    assert len(valid) == len(labels)
    target = ns["suite"](task, valid, invalid)
    mutable = any(s not in ("int", "str", "bytes") for s in task.schemas)
    if not mutable:
        target = target.replace("    before=copy.deepcopy(args)\n", "").replace("    assert args == before\n", "")
        if "copy." not in target:
            target = target.replace("import copy\n", "")
    compile(target, "<repaired-gold>", "exec")
    body = task.contract
    for phrase in (" Do not mutate the input.", " Do not mutate input.", " Do not mutate either input.", " Do not mutate tokens."):
        body = body.replace(phrase, "")
    if ident == "TR041":
        body = body.replace("signed canonical decimal integers", "signed canonical ASCII decimal integers")
    if ident == "TR047":
        body = body.replace("Return the start index", "Matches are literal and case-sensitive. Return the start index")
    schema_text = {
        "int": "exact built-in int; reject bool and int subclasses",
        "str": "exact built-in str; reject str subclasses",
        "bytes": "exact built-in bytes; reject subclasses",
        "ints": "exact list of exact ints; reject bool, int subclasses and list subclasses",
        "strs": "exact list of exact strings; reject list and str subclasses",
        "matrix": "exact list of exact lists of exact ints; reject bool and subclasses at all stated levels",
        "pairs": "exact list of exact two-item tuples of exact ints; reject bool and list/tuple/int subclasses",
        "tuple3": "exact three-item tuple of exact ints; reject bool and tuple/int subclasses",
        "objects": "exact tuple of arbitrary objects; reject tuple subclasses",
    }
    parts = [f"Function contract: {task.name}({', '.join(task.params)})."]
    parts += [f"- {p}: {schema_text[s]}." for p, s in zip(task.params, task.schemas)]
    parts += ["Reject invalid specified types with TypeError before shape/value checks.", body, "Return type: " + B.RETURNS[ident] + "."]
    if mutable:
        parts.append("Do not mutate any input or nested mutable elements.")
    coverage = ("Coverage expectations: include normal cases for " + ", ".join(labels) + ". Test each input position and each stated nested type level "
                "with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated "
                "invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.")
    if mutable:
        coverage += " Compare valid inputs before and after calls."
    parts += [coverage, f"Write one complete pytest file importing 'from subject import {task.name}'. Do not implement, replace, mock or inspect the function. "
              "Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input "
              "mapping and finite-coverage limitations. Do not claim execution."]
    spec_text = "\n\n".join(parts) + "\n"
    mapping = "; ".join(f"{label}={c['id']}" for label, c in zip(labels, valid))
    groups = {exc: [c["id"] for c in invalid if c["exception"] == exc] for exc in sorted({c["exception"] for c in invalid})}
    prose = f"Return cases: {mapping}. Validation cases: " + "; ".join(exc + "=" + ",".join(ids) for exc, ids in groups.items()) + ". Exact returned types are checked recursively where specified."
    if mutable:
        prose += " Valid-input preservation is checked before/after calls."
    prose += " These finite witnesses do not prove exhaustive correctness. No execution is claimed."
    fence = chr(96) * 3
    answer = fence + "python\n" + target + fence + "\n\n" + prose + "\n"
    cases = [dict(id=c["id"], args_python=repr(c["args"]), expected_python=repr(c["expected"]), after_python=repr(c["after"]), category=label) for c, label in zip(valid, labels)]
    cases += [dict(id=c["id"], args_python=repr(c["args"]), exception=c["exception"], category=c["category"]) for c in invalid]
    return dict(split=split, ident=ident, record=record, task=task, reference=reference, labels=labels, valid=valid, invalid=invalid,
                checks=checks, target=target, spec=spec_text, answer=answer, cases=cases, mutable=mutable)


def mutants_as_in_007(a, original):
    """candidate-007's exact mutant derivation (legacy + proposed), for the reproduction check."""
    mutants, proposals = [], []
    for old in json.loads((original / "evaluator/mutants.json").read_text(encoding="utf-8")):
        source = (original / "evaluator/mutants" / old["id"] / "subject.py").read_text(encoding="utf-8")
        witness = B.requirement_witness(source, a["task"], a["valid"], a["invalid"])
        assert witness
        mutants.append(dict(id=old["id"], requirement="legacy-" + old["defect"], source=source, witness=witness,
                            provenance="unchanged candidate-006 mutant; witness refreshed against revised gold"))
    seen = {sha_text(m["source"]) for m in mutants}
    for label, source in B.proposed_mutants(a["reference"], a["task"], a["record"], a["valid"]):
        digest = sha_text(source)
        if digest in seen:
            continue
        witness = B.requirement_witness(source, a["task"], a["valid"], a["invalid"])
        proposals.append(dict(task=a["ident"], requirement=label, status="designated" if witness else "no-relevant-finite-witness", witness=witness))
        if not witness:
            continue
        seen.add(digest)
        mutants.append(dict(id=f"R{len(mutants) - 2:02}", requirement=label, source=source, witness=witness,
                            provenance="S007 requirement-linked fixture; finite witness validated against unchanged reference"))
    return mutants, proposals


def mutants_for_008(a, audit_record):
    """Keep every candidate-007 mutant (same id/source), refresh its witness, then promote audit survivors."""
    folder = C7 / "tasks" / a["split"] / a["ident"]
    mutants, proposals = [], []
    for old in json.loads((folder / "evaluator/mutants.json").read_text(encoding="utf-8")):
        source = (folder / "evaluator/mutants" / old["id"] / "subject.py").read_text(encoding="utf-8")
        assert sha_text(source) == old["source_sha256"]
        witness = B.requirement_witness(source, a["task"], a["valid"], a["invalid"])
        assert witness, (a["ident"], old["id"], "candidate-008 gold lost a candidate-007 witness")
        mutants.append(dict(id=old["id"], requirement=old["requirement"], source=source, witness=witness,
                            provenance=old["provenance"] + "; carried into candidate-008, witness refreshed"))
    seen = {sha_text(m["source"]) for m in mutants}
    next_r = 1 + max([int(m["id"][1:]) for m in mutants if m["id"].startswith("R")] or [0])
    # Regenerate the audit's mutants exactly as the audit did and promote those that survived candidate-007.
    spec7 = (folder / "SPEC.md").read_text(encoding="utf-8")
    value7 = [eval(c["args_python"], dict(probes.NAMESPACE)) for c in json.loads((folder / "evaluator/cases.json").read_text(encoding="utf-8")) if "expected_python" in c]
    base_args = [probes.pyrepr(x) for x in value7[0]]
    _, generated = mutants_lib.build_mutants(a["ident"], a["reference"], spec7, base_args, set(audit_record["reference_raises"]), audit_record["return_depth"])
    by_id = {m["id"]: m for m in generated}
    for entry in audit_record["mutants"]:
        if entry["status"] != "differs" or entry["family"] not in R8.PROMOTED_FAMILIES:
            continue
        if entry["gold"]["candidate-007"]["verdict"] != "passed":
            continue
        source = by_id[entry["id"]]["source"]
        assert sha_text(source) == entry["source_sha256"], (a["ident"], entry["id"], "audit mutant not reproduced")
        witness = B.requirement_witness(source, a["task"], a["valid"], a["invalid"])
        proposals.append(dict(task=a["ident"], audit_mutant=entry["id"], family=entry["family"], requirement=entry["requirement"],
                              status="designated" if witness else "still-surviving", witness=witness))
        if not witness or sha_text(source) in seen:
            continue
        seen.add(sha_text(source))
        mutants.append(dict(id=f"R{next_r:02}", requirement=f"{entry['family']}: {entry['requirement']}", source=source, witness=witness,
                            provenance=f"S010 promotion of independent-audit mutant {entry['id']} (independent-review/c007-rubric-audit); "
                                       "survived candidate-007 gold; finite witness validated against unchanged reference"))
        next_r += 1
    return mutants, proposals


def tasks():
    for split in ("training", "development"):
        for original in sorted((C6 / "tasks" / split).iterdir()):
            yield split, original


def reproduce_007():
    """Regenerate candidate-007 code/case/prompt files and compare bytes."""
    compared, mismatched = 0, []
    for split, original in tasks():
        a = assemble_task(split, original, additions=False)
        mutants, _ = mutants_as_in_007(a, original)
        folder = C7 / "tasks" / split / a["ident"]
        expected = {"SPEC.md": a["spec"], "PROMPT.md": B.SYSTEM + "\n\n" + a["spec"], "TARGET.md": a["answer"], "test_target.py": a["target"],
                    "evaluator/cases.json": json.dumps(a["cases"], indent=2, ensure_ascii=False) + "\n",
                    "evaluator/reference/subject.py": a["reference"]}
        manifest = [{k: v for k, v in m.items() if k != "source"} | dict(source_sha256=sha_text(m["source"])) for m in mutants]
        expected["evaluator/mutants.json"] = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
        for m in mutants:
            expected[f"evaluator/mutants/{m['id']}/subject.py"] = m["source"]
        for name, text in expected.items():
            compared += 1
            if (folder / name).read_text(encoding="utf-8") != text:
                mismatched.append(f"{a['ident']}/{name}")
    return {"files_compared": compared, "mismatched": mismatched, "identical": not mismatched}


def build():
    assert not C8.exists(), "Refuse to overwrite an existing candidate-008"
    audit = json.loads((AUDIT / "results" / "audit-results.json").read_text(encoding="utf-8"))["tasks"]
    artifacts, reports, proposals = {}, [], []
    for split, original in tasks():
        a = assemble_task(split, original, additions=True)
        mutants, props = mutants_for_008(a, audit[a["ident"]])
        proposals += props
        prev = json.loads((C7 / "tasks" / split / a["ident"] / "record.json").read_text(encoding="utf-8"))
        a["mutants"] = mutants
        a["record_out"] = {**prev, "revision": prev.get("revision", 2) + 1, "status": "repair-candidate-unapproved",
                           "review_status": "finite-agent-calibration-pending-execution", "training_eligible": False,
                           "parent_candidate": "candidate-007", "source_sha256": sha_text(a["reference"]), "spec_sha256": sha_text(a["spec"]),
                           "target_sha256": sha_text(a["target"]), "answer_sha256": sha_text(a["answer"]), "valid_test_cases": len(a["valid"]),
                           "exception_test_cases": len(a["invalid"]), "designated_mutants": len(mutants), "oracle_checks": a["checks"],
                           "type_before_value_witnesses": sum(c.get("category") == "type-before-value" for c in a["cases"]),
                           "pytest_validation": "pending S010 validation",
                           "provenance": "Contract/oracle-authored derivative of candidate-007 (S010 declared additions); no failed model output used as a training answer."}
        for stale in ("pytest_validation",):
            pass
        a["rubric"] = dict(status="finite-agent-category-map-pending-execution", model_visible=True, return_type=B.RETURNS[a["ident"]],
                           semantic_categories=[dict(requirement=l, gold_case=c["id"]) for l, c in zip(a["labels"], a["valid"])],
                           type_coverage="Every stated argument/type level: ordinary and subclass; bool for int; other arguments valid.",
                           validation_order="Type checks before value/shape; stated shape checks before bounds.", mutation_applicable=a["mutable"],
                           limitations="Finite same-agent semantic review plus one independent-audit mutant pass; not exhaustive correctness.")
        added_valid = [l for _, l in R8.VALID_008.get(a["ident"], [])]
        added_invalid = [l for _, _, l in R8.INVALID_008.get(a["ident"], [])]
        reports.append(dict(id=a["ident"], split=split, source_reference_unchanged=True, source_hash=sha_text(a["reference"]),
                            valid_cases=len(a["valid"]), invalid_cases=len(a["invalid"]), oracle_checks=a["checks"], semantic_categories=a["labels"],
                            added_valid_labels=added_valid, added_invalid_labels=added_invalid, mutants=len(mutants),
                            promoted_mutants=[m["id"] for m in mutants if m["provenance"].startswith("S010")]))
        artifacts[a["ident"]] = a
    assert len(artifacts) == 72
    staging = pathlib.Path(tempfile.mkdtemp(prefix="candidate-008-", dir=DATA))
    try:
        for ident, a in artifacts.items():
            folder = staging / "tasks" / a["split"] / ident
            B.write(folder / "SPEC.md", a["spec"]); B.write(folder / "PROMPT.md", B.SYSTEM + "\n\n" + a["spec"])
            B.write(folder / "TARGET.md", a["answer"]); B.write(folder / "test_target.py", a["target"])
            B.dump(folder / "record.json", a["record_out"]); B.dump(folder / "rubric.json", a["rubric"])
            B.dump(folder / "evaluator/cases.json", a["cases"]); B.write(folder / "evaluator/reference/subject.py", a["reference"])
            manifest = []
            for m in a["mutants"]:
                B.write(folder / "evaluator/mutants" / m["id"] / "subject.py", m["source"])
                manifest.append({k: v for k, v in m.items() if k != "source"} | dict(source_sha256=sha_text(m["source"])))
            B.dump(folder / "evaluator/mutants.json", manifest)
            for name in ("oracle.py", "oracle-inputs.json", "oracle-check.json"):
                shutil.copyfile(C7 / "tasks" / a["split"] / ident / "evaluator" / name, folder / "evaluator" / name)
        for split in ("training", "development"):
            packets = [dict(id=i, family=a["record_out"]["family"], messages=[dict(role="system", content=B.SYSTEM), dict(role="user", content=a["spec"])]
                            + ([dict(role="assistant", content=a["answer"])] if split == "training" else [])) for i, a in artifacts.items() if a["split"] == split]
            B.write(staging / "model-packets" / (split + "-requests.jsonl"), "\n".join(json.dumps(p, ensure_ascii=False) for p in packets) + "\n")
        (staging / "build-sources").mkdir()
        for p in (pathlib.Path(__file__), HERE / "repair_config_008.py", HERE / "PROTOCOL.md"):
            shutil.copyfile(p, staging / "build-sources" / p.name)
        B.dump(staging / "manifest.json", dict(candidate="candidate-008", scope="training/development only; final/regression omitted and untouched",
                                              parent="candidate-007", status="pending-calibration-validation",
                                              training_authorization="none; not exported or approved under any prior corpus hash",
                                              tasks=[a["record_out"] for a in artifacts.values()]))
        B.dump(staging / "calibration-design.json", dict(tasks=reports, promoted_audit_mutants=proposals, deferred=R8.DEFERRED,
                                                         review_limit="same coordinating agent; one independent-audit pass informed the additions"))
        B.write(staging / "README.md", "# Candidate 008 — rubric-gap repair draft, not a training export\n\n"
                "Derivative of candidate-007 adding the gold cases and designated mutants listed in build-sources/repair_config_008.py. "
                "Correct implementations are unchanged. Final/regression tasks are omitted. See ../../studies/S010-rubric-gap-repair/.\n\n"
                "Status: pending calibration validation. No training approval or export is implied; CURRENT_CANDIDATE.txt is unchanged.\n")
        hashes = {p.relative_to(staging).as_posix(): sha(p) for p in staging.rglob("*") if p.is_file()}
        B.dump(staging / "SHA256.json", hashes)
        staging.rename(C8)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    report = dict(status="built-pending-execution", parent="candidate-007", tasks=reports,
                  candidate_hash_manifest_sha256=sha(C8 / "SHA256.json"),
                  designated_mutants=sum(r["mutants"] for r in reports),
                  promoted_audit_mutants=sum(len(r["promoted_mutants"]) for r in reports),
                  still_surviving_audit_mutants=[p for p in proposals if p["status"] == "still-surviving"],
                  valid_cases=sum(r["valid_cases"] for r in reports), invalid_cases=sum(r["invalid_cases"] for r in reports),
                  oracle_checks=sum(r["oracle_checks"] for r in reports))
    B.dump(HERE / "build-report.json", report)
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reproduce-007", action="store_true", help="only run the candidate-007 equivalence check")
    args = parser.parse_args()
    check = reproduce_007()
    print(json.dumps({k: (v[:20] if isinstance(v, list) else v) for k, v in check.items()}, indent=2))
    assert check["identical"], "builder does not reproduce candidate-007; refusing to build"
    B.dump(HERE / "reproduce-007.json", check)
    if args.reproduce_007:
        return
    report = build()
    print(json.dumps({k: report[k] for k in ("designated_mutants", "promoted_audit_mutants", "valid_cases", "invalid_cases", "oracle_checks")}, indent=2))
    print("still surviving:", [(p["task"], p["audit_mutant"]) for p in report["still_surviving_audit_mutants"]])


if __name__ == "__main__":
    main()
