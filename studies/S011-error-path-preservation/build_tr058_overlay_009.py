"""TR058 presentation fit overlay for candidate-009: the S010 builder, unchanged, pointed at candidate-009.

Only the mapping prose adds the S011 preservation sentence. Same gates: executable AST equal to the
candidate-009 gold ignoring display ids, and identical per-case results for the reference and every
designated mutant. Token counting happens in the cloud workflow.
"""
import importlib.util, pathlib, sys
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
EXP = HERE.parents[1]
spec = importlib.util.spec_from_file_location("s010_overlay", EXP / "studies/S010-rubric-gap-repair/build_tr058_overlay.py")
o = importlib.util.module_from_spec(spec); spec.loader.exec_module(o)
o.C8 = EXP / "dataset-v1" / "candidate-009"
o.TASK = o.C8 / "tasks" / "training" / "TR058"
o.OUT = HERE / "tr058-fit-overlay"
o.PROSE = o.PROSE.replace("Exact int return is checked.", "Exact int return is checked; inputs are compared before and after every call, including expected-exception calls.")
assert "including expected-exception calls" in o.PROSE
if __name__ == "__main__":
    o.main()
    import json
    path = o.OUT / "validation.json"
    report = json.loads(path.read_text(encoding="utf-8"))
    report.update(parent_candidate="candidate-009", scope="Presentation overlay only; candidate-009 files unchanged; not an export or training authorization.")
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
