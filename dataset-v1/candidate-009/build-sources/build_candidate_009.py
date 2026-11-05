"""CPU-only candidate-009 builder: candidate-008 plus error-path input preservation (audit finding N7).

    python studies/S011-error-path-preservation/build_candidate_009.py

For the 19 tasks with mutable inputs (those whose coverage expectations said
"Compare valid inputs before and after calls."):
  * model-visible SPEC/PROMPT: that sentence becomes PRESERVE_SENTENCE (the contract already said
    "Do not mutate any input or nested mutable elements.");
  * gold: every test_raises_* function snapshots args with copy.deepcopy and asserts they are unchanged
    after the expected exception;
  * TARGET.md: the code block is the new gold and the preservation prose is updated;
  * mutants: all candidate-008 mutants are kept (same ids/sources); the independent audit's
    "mutation-error" mutants are regenerated, hash-checked and promoted with a declared witness
    (expected exception raised but an argument changed).
The other 53 tasks are copied unchanged. References, cases and oracle files are unchanged.
Refuses to overwrite. Final/regression tasks are never read.
"""
import sys
sys.dont_write_bytecode = True
import copy, hashlib, json, pathlib, re, shutil, tempfile

HERE = pathlib.Path(__file__).resolve().parent
EXP = HERE.parents[1]
DATA = EXP / "dataset-v1"
C8, C9 = DATA / "candidate-008", DATA / "candidate-009"
AUDIT = EXP / "independent-review" / "c007-rubric-audit"
sys.path.insert(0, str(AUDIT))
import mutants_lib  # noqa: E402
import probes      # noqa: E402

OLD_SENTENCE = "Compare valid inputs before and after calls."
PRESERVE_SENTENCE = "Compare inputs before and after every call, including calls that raise."
OLD_PROSE = "Valid-input preservation is checked before/after calls."
NEW_PROSE = "Input preservation is checked before/after every call, including expected-exception calls."
RAISES = re.compile(r"(def test_raises_(\w+)\(args\):\n)    with pytest\.raises\((\w+)\):\n        (\w+)\(\*args\)\n")


def sha_text(text):
    return hashlib.sha256(text.encode()).hexdigest()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strengthen(gold):
    new, count = RAISES.subn(lambda m: f"{m.group(1)}    before=copy.deepcopy(args)\n    with pytest.raises({m.group(3)}):\n"
                                       f"        {m.group(4)}(*args)\n    assert args == before\n", gold)
    assert count >= 1 and "import copy\n" in new
    compile(new, "<s011-gold>", "exec")
    return new


def run_function(source, name, args):
    namespace = {}
    exec(compile(source, "<s011-fixture>", "exec"), namespace)
    working = copy.deepcopy(args)
    try:
        result = namespace[name](*working)
        return "return", result, working
    except Exception as error:  # noqa: BLE001 - the exception class is the observable
        return "raise", type(error).__name__, working


def error_path_witness(source, name, cases):
    """First invalid case where the expected exception is raised but an argument changed."""
    for case in cases:
        if "exception" not in case:
            continue
        args = eval(case["args_python"], dict(probes.NAMESPACE))
        kind, value, after = run_function(source, name, args)
        if kind == "raise" and value == case["exception"] and probes.canon(after) != probes.canon(args):
            return dict(node=f"test_target.py::test_raises_{case['exception'].lower()}[{case['id']}]", case=case["id"],
                        kind="input-mutated-on-expected-exception", args_python=case["args_python"],
                        expected_exception=case["exception"], args_after_python=probes.pyrepr(after))
    return None


def main():
    assert not C9.exists(), "refuse to overwrite candidate-009"
    digests = json.loads((C8 / "SHA256.json").read_text(encoding="utf-8"))
    for name, digest in digests.items():
        assert sha(C8 / name) == digest, f"candidate-008 changed: {name}"
    audit = json.loads((AUDIT / "results" / "audit-results.json").read_text(encoding="utf-8"))["tasks"]
    staging = pathlib.Path(tempfile.mkdtemp(prefix="candidate-009-", dir=DATA))
    shutil.rmtree(staging); shutil.copytree(C8, staging)
    try:
        for p in ("SHA256.json", "README.md", "manifest.json", "calibration-design.json"):
            (staging / p).unlink()
        shutil.rmtree(staging / "build-sources")
        reports = []
        for split in ("training", "development"):
            for task in sorted((staging / "tasks" / split).iterdir()):
                spec = (task / "SPEC.md").read_text(encoding="utf-8")
                if OLD_SENTENCE not in spec:
                    continue
                ident = task.name
                record = json.loads((task / "record.json").read_text(encoding="utf-8"))
                gold = strengthen((task / "test_target.py").read_text(encoding="utf-8"))
                spec = spec.replace(OLD_SENTENCE, PRESERVE_SENTENCE)
                prompt = (task / "PROMPT.md").read_text(encoding="utf-8").replace(OLD_SENTENCE, PRESERVE_SENTENCE)
                answer = (task / "TARGET.md").read_text(encoding="utf-8")
                fence = chr(96) * 3
                head, rest = answer.split(fence + "python\n", 1)
                _, prose = rest.split(fence + "\n", 1)
                assert OLD_PROSE in prose
                answer = head + fence + "python\n" + gold + fence + "\n" + prose.replace(OLD_PROSE, NEW_PROSE)
                for name, text in (("SPEC.md", spec), ("PROMPT.md", prompt), ("TARGET.md", answer), ("test_target.py", gold)):
                    (task / name).write_text(text, encoding="utf-8", newline="\n")
                cases = json.loads((task / "evaluator/cases.json").read_text(encoding="utf-8"))
                mutants = json.loads((task / "evaluator/mutants.json").read_text(encoding="utf-8"))
                reference = (task / "evaluator/reference/subject.py").read_text(encoding="utf-8")
                info = mutants_lib.parse_reference(reference)
                next_r = 1 + max(int(m["id"][1:]) for m in mutants if m["id"].startswith("R"))
                c7 = DATA / "candidate-007" / "tasks" / split / ident
                value7 = [eval(c["args_python"], dict(probes.NAMESPACE)) for c in json.loads((c7 / "evaluator/cases.json").read_text(encoding="utf-8")) if "expected_python" in c]
                _, generated = mutants_lib.build_mutants(ident, reference, (c7 / "SPEC.md").read_text(encoding="utf-8"),
                                                         [probes.pyrepr(x) for x in value7[0]], set(audit[ident]["reference_raises"]), audit[ident]["return_depth"])
                by_id = {m["id"]: m for m in generated}
                promoted, surviving = [], []
                for entry in audit[ident]["mutants"]:
                    if entry["family"] != "mutation-error" or entry["status"] != "differs":
                        continue
                    source = by_id[entry["id"]]["source"]
                    assert sha_text(source) == entry["source_sha256"], (ident, entry["id"])
                    witness = error_path_witness(source, info["name"], cases)
                    if not witness:
                        surviving.append(entry["id"]); continue
                    mid = f"R{next_r:02}"; next_r += 1
                    (task / "evaluator/mutants" / mid).mkdir(parents=True)
                    (task / "evaluator/mutants" / mid / "subject.py").write_text(source, encoding="utf-8", newline="\n")
                    mutants.append(dict(id=mid, requirement=f"mutation-error: {entry['requirement']}", witness=witness,
                                        provenance=f"S011 promotion of independent-audit mutant {entry['id']}; survived candidate-007/008 gold; "
                                                   "witness: expected exception raised but an argument changed",
                                        source_sha256=sha_text(source)))
                    promoted.append(mid)
                (task / "evaluator/mutants.json").write_text(json.dumps(mutants, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
                record.update(revision=record["revision"] + 1, status="repair-candidate-unapproved", training_eligible=False, parent_candidate="candidate-008",
                              spec_sha256=sha_text(spec), target_sha256=sha_text(gold), answer_sha256=sha_text(answer), designated_mutants=len(mutants),
                              review_status="finite-agent-calibration-pending-execution", pytest_validation="pending S011 validation",
                              provenance="Candidate-008 plus S011 error-path preservation (prompt sentence, gold assertion, promoted audit mutants).")
                (task / "record.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
                rubric = json.loads((task / "rubric.json").read_text(encoding="utf-8"))
                rubric.update(status="finite-agent-category-map-pending-execution", mutation_scope="valid and expected-exception calls")
                (task / "rubric.json").write_text(json.dumps(rubric, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
                reports.append(dict(id=ident, split=split, raise_tests_strengthened=gold.count("assert args == before") - 1,
                                    promoted_mutants=promoted, still_surviving=surviving, designated_mutants=len(mutants)))
        # model packets from the (possibly changed) SPEC/TARGET files
        for split in ("training", "development"):
            rows = []
            for line in (C8 / "model-packets" / f"{split}-requests.jsonl").read_text(encoding="utf-8").splitlines():
                row = json.loads(line)
                task = staging / "tasks" / split / row["id"]
                row["messages"][1]["content"] = (task / "SPEC.md").read_text(encoding="utf-8")
                if split == "training":
                    row["messages"][2]["content"] = (task / "TARGET.md").read_text(encoding="utf-8")
                rows.append(json.dumps(row, ensure_ascii=False))
            (staging / "model-packets" / f"{split}-requests.jsonl").write_text("\n".join(rows) + "\n", encoding="utf-8")
        (staging / "build-sources").mkdir()
        for p in (pathlib.Path(__file__), HERE / "PROTOCOL.md"):
            shutil.copyfile(p, staging / "build-sources" / p.name)
        manifest = json.loads((C8 / "manifest.json").read_text(encoding="utf-8"))
        manifest.update(candidate="candidate-009", parent="candidate-008", status="pending-calibration-validation",
                        training_authorization="none; requires explicit approval of the changed prompt sentence and of this hash",
                        tasks=[json.loads(p.read_text(encoding="utf-8")) for p in sorted((staging / "tasks").glob("*/*/record.json"))])
        (staging / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (staging / "calibration-design.json").write_text(json.dumps(dict(changed_tasks=reports, old_sentence=OLD_SENTENCE, new_sentence=PRESERVE_SENTENCE,
                                                                        old_prose=OLD_PROSE, new_prose=NEW_PROSE), indent=2) + "\n", encoding="utf-8")
        (staging / "README.md").write_text("# Candidate 009 — error-path preservation proposal, not a training export\n\n"
                                           "Candidate-008 plus audit finding N7 for the 19 mutable-input tasks: one changed coverage sentence, "
                                           "a before/after assertion on every expected-exception test, and promoted audit mutants. "
                                           "Requires explicit user approval of the prompt change and of this hash. See ../../studies/S011-error-path-preservation/.\n",
                                           encoding="utf-8")
        hashes = {p.relative_to(staging).as_posix(): sha(p) for p in sorted(staging.rglob("*")) if p.is_file()}
        (staging / "SHA256.json").write_text(json.dumps(hashes, indent=2) + "\n", encoding="utf-8")
        staging.rename(C9)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    report = dict(status="built-pending-execution", parent="candidate-008", changed_tasks=len(reports),
                  promoted_mutants=sum(len(r["promoted_mutants"]) for r in reports),
                  still_surviving=[(r["id"], s) for r in reports for s in r["still_surviving"]],
                  candidate_hash_manifest_sha256=sha(C9 / "SHA256.json"), tasks=reports)
    (HERE / "build-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "tasks"}, indent=2))


if __name__ == "__main__":
    main()
