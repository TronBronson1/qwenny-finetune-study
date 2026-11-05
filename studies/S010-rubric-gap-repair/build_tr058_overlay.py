"""Presentation-only TR058 fit overlay for candidate-008 (same method as S007 length-preview-002).

    python studies/S010-rubric-gap-repair/build_tr058_overlay.py

Removes pytest display ids, blank lines and ", " spacing from the candidate-008 TR058 gold and
shortens the mapping prose. Gates (all required, nothing in candidate-008 is changed):
  * executable AST equal to the candidate-008 gold, ignoring only pytest.param ids;
  * per-test-case result vector identical to the candidate-008 gold for the reference and every
    designated mutant (pytest, plugin autoload off, isolated temp dirs);
Token counting needs the pinned tokenizer and is done by profile_lengths_cloud.py (GitHub Actions).
"""
import ast, copy, hashlib, json, os, pathlib, re, shutil, subprocess, sys, tempfile
import xml.etree.ElementTree as ET

HERE = pathlib.Path(__file__).resolve().parent
EXP = HERE.parents[1]
C8 = EXP / "dataset-v1" / "candidate-008"
TASK = C8 / "tasks" / "training" / "TR058"
OUT = HERE / "tr058-fit-overlay"

PROSE = ("Equal versions return 0; (1,2,3)/(1,2,4) returns -1; (1,3,0)/(1,2,99) and (2,0,0)/(1,99,99) return 1. "
         "TypeError cases isolate ordinary wrong types (including lists for tuples), bool and subclasses at the stated "
         "argument/component levels, including type-before-value witnesses. ValueError cases cover tuple shape and negative "
         "components. Exact int return is checked. Finite cases are not exhaustive. No execution is claimed.")


def normalized(text):
    tree = ast.parse(text)
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name) \
                and n.func.value.id == "pytest" and n.func.attr == "param":
            n.keywords = [k for k in n.keywords if k.arg != "id"]
    return ast.dump(tree, include_attributes=False)


def vector(test_text, subject):
    with tempfile.TemporaryDirectory(prefix="tr058-", ignore_cleanup_errors=True) as tmp:
        tmp = pathlib.Path(tmp)
        (tmp / "test_target.py").write_text(test_text, encoding="utf-8", newline="\n")
        shutil.copyfile(subject, tmp / "subject.py"); (tmp / "pytest.ini").write_text("[pytest]\n")
        env = {k: v for k, v in os.environ.items() if not k.startswith("PYTEST")}
        env.update(PYTEST_DISABLE_PLUGIN_AUTOLOAD="1", PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1")
        run = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-c", str(tmp / "pytest.ini"),
                              "--rootdir", str(tmp), "--junitxml", str(tmp / "r.xml"), "test_target.py"],
                             cwd=tmp, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
        cases = [(t.attrib["name"].split("[")[0], t.find("failure") is not None, t.find("error") is not None, t.find("skipped") is not None)
                 for t in ET.parse(tmp / "r.xml").findall(".//testcase")]
        return run.returncode, cases


def main():
    assert not OUT.exists(), "refuse to overwrite"
    digests = json.loads((C8 / "SHA256.json").read_text(encoding="utf-8"))
    for name in ("tasks/training/TR058/test_target.py", "model-packets/training-requests.jsonl"):
        assert hashlib.sha256((C8 / name).read_bytes()).hexdigest() == digests[name], name
    gold = (TASK / "test_target.py").read_text(encoding="utf-8")
    compact = re.sub(r''',\s*id\s*=\s*(['"])[^'"\n]*\1''', "", gold)
    compact = "\n".join(line.rstrip() for line in compact.splitlines() if line.strip()) + "\n"
    compact = re.sub(r", +", ",", compact)
    assert normalized(gold) == normalized(compact), "executable AST changed"
    fence = chr(96) * 3
    answer = fence + "python\n" + compact + fence + "\n\n" + PROSE + "\n"
    row = next(json.loads(x) for x in (C8 / "model-packets/training-requests.jsonl").read_text(encoding="utf-8").splitlines() if json.loads(x)["id"] == "TR058")
    messages = copy.deepcopy(row["messages"]); messages[-1]["content"] = answer
    variants = [("reference", TASK / "evaluator/reference/subject.py")] + \
               [(m["id"], TASK / "evaluator/mutants" / m["id"] / "subject.py") for m in json.loads((TASK / "evaluator/mutants.json").read_text(encoding="utf-8"))]
    results = []
    for name, subject in variants:
        code_gold, vec_gold = vector(gold, subject)
        code_compact, vec_compact = vector(compact, subject)
        assert code_gold == code_compact == (0 if name == "reference" else 1), (name, code_gold, code_compact)
        assert vec_gold == vec_compact, (name, "per-case result vector changed")
        results.append(dict(variant=name, exit_code=code_compact, cases=len(vec_compact), per_case_results_identical=True))
    OUT.mkdir()
    (OUT / "test_target.py").write_text(compact, encoding="utf-8", newline="\n")
    (OUT / "TARGET.md").write_text(answer, encoding="utf-8", newline="\n")
    (OUT / "messages.json").write_text(json.dumps(messages, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report = dict(status="passed-pending-token-count", task="TR058", parent_candidate="candidate-008",
                  parent_sha256=hashlib.sha256((C8 / "SHA256.json").read_bytes()).hexdigest(),
                  messages_sha256=hashlib.sha256((OUT / "messages.json").read_bytes()).hexdigest(),
                  executable_ast_equal_ignoring_display_ids=True, variants=results,
                  scope="Presentation overlay only; candidate-008 files unchanged; not an export or training authorization.")
    (OUT / "validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "variants"} | {"variants": len(results)}, indent=2))


if __name__ == "__main__":
    main()
