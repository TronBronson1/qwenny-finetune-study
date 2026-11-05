"""Declared candidate-008 additions on top of candidate-007's repair_config.

Every entry closes a gap found by independent-review/c007-rubric-audit (finding ids N1-N6).
Inputs were chosen from the contract and the audit's confirmed witnesses; expected values are
computed by the separate original oracle at build time and asserted equal to the unchanged
reference. No model answer is used as a target. Final/regression tasks are not referenced.
"""

# New normal-return cases: ident -> [(args, label)]. Labels become part of the model-visible
# coverage list, exactly as in candidate-007.
VALID_008 = {
    # N4: valid-call input mutation hidden by already-sorted inputs.
    "TR029": [(([4, 2], 2), "unsorted-values")],
    "TR030": [(([[2, 1], [0, 3]],), "unsorted-rows")],
    "TR033": [(([4, 2], 0), "unsorted-values")],
    "TR034": [(([3, 1, 2], 0, 3), "unsorted-values")],
    # N5: boundaries / merge logic.
    "DV010": [((["9999"],), "maximum-digits"), ((["-9999"],), "negative-maximum-digits")],
    "DV011": [(([(1, 4), (2, 6)],), "partial-overlap"),
              (([(2, 60), (-3, -1), (10, 100)],), "unordered-overlap-chain"),
              (([(1, 2), (26, 27), (25, 130), (25, 256)],), "shared-low-overlap")],
    # N6: literal character preservation / ASCII-only classification stated in the contract.
    "TR014": [(("a\n\nb",), "preserve-lf-run"), (("a\t\tb",), "preserve-tab-run"), (("a \t\nb",), "space-then-tab-lf"), (("٣  ４",), "unicode-digits")],
    "TR015": [(("١  ｅ",), "unicode-word-content")],
    "TR016": [(("Ｅá",), "fullwidth-and-accented")],
    "TR024": [(("ǅ١ｅ",), "compatibility-characters")],
    "TR060": [(("ǅＡ١",), "compatibility-characters")],
}

# New invalid cases: ident -> [(args, exception, label)].
INVALID_008 = {
    # N1: non-ASCII digit in a non-leading position ([0-9] -> \d survives in 007).
    "TR037": [(("1٠",), "ValueError", "ascii-nonleading-digit")],
    "TR041": [(("1٠,2",), "ValueError", "ascii-nonleading-digit"), (("1,2٠",), "ValueError", "ascii-nonleading-digit")],
    "TR042": [(("1٠.0.0",), "ValueError", "ascii-nonleading-digit"), (("0.0.1٠",), "ValueError", "ascii-nonleading-digit")],
    "TR044": [(("[0:1٠]",), "ValueError", "ascii-nonleading-digit"), (("[1٠:20]",), "ValueError", "ascii-nonleading-digit")],
    # N2: ordinary wrong types that duck-typed code would accept or misreport.
    "DV005": [((["("],), "TypeError", "ordinary-iterable")],
    "DV006": [((["A"],), "TypeError", "ordinary-iterable")],
    "DV012": [((["("],), "TypeError", "ordinary-iterable")],
    "TR014": [((["a"],), "TypeError", "ordinary-iterable")],
    "TR016": [((["a"],), "TypeError", "ordinary-iterable")],
    "TR017": [((["a"], "b"), "TypeError", "ordinary-iterable"), (("a", ["b"]), "TypeError", "ordinary-iterable")],
    "TR020": [((["a"],), "TypeError", "ordinary-iterable")],
    "TR022": [((["a"],), "TypeError", "ordinary-iterable")],
    "TR024": [((["a"],), "TypeError", "ordinary-iterable")],
    "TR057": [((["a"],), "TypeError", "ordinary-iterable")],
    "TR060": [((["a"],), "TypeError", "ordinary-iterable")],
    "TR006": [((-1.5,), "TypeError", "ordinary-before-domain")],
    "TR008": [((-1.5,), "TypeError", "ordinary-before-domain")],
    "TR010": [((-1.5,), "TypeError", "ordinary-before-domain")],
    "TR013": [((-1.5, 2), "TypeError", "ordinary-before-domain")],
    "TR048": [((-1.5,), "TypeError", "ordinary-before-domain")],
    "TR023": [((-1, 1), "TypeError", "ordinary-before-domain")],
    "TR029": [(([1], -1.5), "TypeError", "ordinary-before-domain")],
    "TR030": [(((),), "TypeError", "ordinary-container"), (([(1,)],), "TypeError", "ordinary-row"),
              (([[1], None, [1, 2]],), "TypeError", "type-before-shape")],
    "TR058": [(([0, 0, 0], (0, 0, 0, 0)), "TypeError", "ordinary-container-before-shape"),
              (((0, 0), [0, 0, 0]), "TypeError", "ordinary-container-before-shape")],
    "TR059": [(((2, 1), []), "TypeError", "ordinary-container-before-order"),
              (([], (2, 1)), "TypeError", "ordinary-container-before-order")],
    # N2/N3: order witnesses mixing a type error with a value/shape error.
    "DV004": [(([-1, "x"],), "TypeError", "type-before-value")],
    "DV010": [((["+", 1],), "TypeError", "type-before-value"),
              ((["10000"],), "ValueError", "digit-length"),
              ((["4", "+"],), "ValueError", "insufficient-operands")],
    "DV011": [(((),), "TypeError", "ordinary-container"), (([[1, 2]],), "TypeError", "ordinary-pair"),
              (([(1,), -1],), "TypeError", "type-before-shape")],
    # N5: boundaries.
    "DV007": [((0, 1, 1, 1), "IndexError", "column-equals-columns"), ((1, 0, 1, 1), "IndexError", "row-equals-rows")],
    "TR050": [((0, 1, 0), "ValueError", "columns-zero")],
}

# Audit families promoted to designated mutants when the revised gold kills them.
PROMOTED_FAMILIES = ("type-ordinary", "order", "mutation-valid", "ascii", "boundary")

DEFERRED = {
    "mutation-error": ("N7: input mutation before raising. The model-visible coverage expectations limit "
                       "before/after checks to valid inputs, so adding these witnesses would change the "
                       "task instructions as well as the gold. Deferred to a separately declared prompt revision."),
}
