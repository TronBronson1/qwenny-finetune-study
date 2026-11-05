import importlib.util, sys
def load(task, variant):
    spec = importlib.util.spec_from_file_location(task + variant, f"{task}/{variant}/subject.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
class IntChild(int): pass
cases = [
 ("training_TR038", "parse_hex_byte", ("٣f",)),
 ("training_TR043", "parse_binary", ("١٠",)),
 ("training_TR044", "parse_range", ("[٣:7]",)),
 ("training_TR056", "decode_rgb", ("#٠٠ff00",)),
 ("development_DV010", "rpn_evaluate", (["٣", "4", "+"],)),
 ("development_DV008", "edit_distance", ("A", "a")),
 ("development_DV011", "interval_union", ([(IntChild(0), 2)],)),
 ("training_TR027", "pairwise_differences", (["x"],)),
]
for task, fn, args in cases:
    out = []
    for v in ("reference", "rubric_mutant"):
        try: out.append(repr(getattr(load(task, v), fn)(*args)))
        except Exception as e: out.append(type(e).__name__)
    print(f"{task:20s} {fn}{tuple(ascii(a) for a in args)}: reference={out[0]}  mutant={out[1]}")
