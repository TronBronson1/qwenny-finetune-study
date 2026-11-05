"""Calibration gate for candidate-009: the S010 validator, unchanged, pointed at candidate-009.

    python studies/S011-error-path-preservation/validate_candidate_009.py [--out DIR] [--note TEXT]
"""
import importlib.util, pathlib, sys
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
EXP = HERE.parents[1]
spec = importlib.util.spec_from_file_location("s010_validator", EXP / "studies/S010-rubric-gap-repair/validate_candidate_008.py")
v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
v.C8 = EXP / "dataset-v1" / "candidate-009"
v.OUT = HERE / "validation-001"
if __name__ == "__main__":
    v.main()
