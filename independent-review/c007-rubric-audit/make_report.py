#!/usr/bin/env python3
"""Turn results/audit-results.json into results/summary.json and results/TABLES.md."""
import collections
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
C6, C7 = "candidate-006", "candidate-007"

# Known gaps from program/reviews/review-002 (behavioural) and its 16-task structural ordinary-element list.
KNOWN_BEHAVIOURAL = {
    "TR038": ("non-ASCII hex digits accepted", lambda m: m["family"] == "ascii"),
    "TR043": ("non-ASCII binary digits accepted", lambda m: m["family"] == "ascii"),
    "TR044": ("non-ASCII decimal endpoints accepted", lambda m: m["family"] == "ascii"),
    "TR056": ("non-ASCII RGB hex digits accepted", lambda m: m["family"] == "ascii"),
    "DV010": ("non-ASCII RPN digits accepted", lambda m: m["family"] == "ascii"),
    "DV008": ("case-insensitive comparison", lambda m: m["id"].startswith("C-input")),
    "DV011": ("int-subclass endpoints accepted", lambda m: m["id"] == "T-intervals-L2-subclass"),
}
ORDINARY_16 = ["TR026", "TR027", "TR028", "TR029", "TR030", "TR031", "TR032", "TR033", "TR034",
               "TR035", "TR036", "TR058", "TR059", "DV004", "DV009", "DV011"]


def item_level_ordinary(m, record):
    if m["family"] != "type-ordinary":
        return False
    # element level = deepest stated level of a list/tuple schema argument
    deepest = {"ints": 1, "matrix": 2, "pairs": 2, "tuple3": 1, "strs": 1}
    for param, schema in zip(record["params"], record["schemas"]):
        if schema in deepest and m["id"] == f"T-{param}-L{deepest[schema]}-ordinary":
            return True
    return False


def verdict(m, candidate):
    return m.get("gold", {}).get(candidate, {}).get("verdict")


def status_of(mutants, candidate):
    """Return 'gap' if any applicable mutant passes the gold, 'covered' if all are killed, 'n/a' otherwise."""
    applicable = [m for m in mutants if m["status"] == "differs"]
    if not applicable:
        return "n/a"
    return "gap" if any(verdict(m, candidate) == "passed" for m in applicable) else "covered"


def main():
    data = json.loads((RESULTS / "audit-results.json").read_text())
    tasks = data["tasks"]
    families = collections.OrderedDict()
    per_task = []
    open_gaps, fixed_gaps, new_gaps, anomalies = [], [], [], []
    for tid, record in sorted(tasks.items()):
        row = {"task": tid, "split": record["split"], "function": record["function"], "mutants": len(record["mutants"]),
               "applicable": 0, "no_difference": 0, "gaps": {C6: [], C7: []}, "fixed": [], "still_open": [], "new_in_007": []}
        for cand in (C6, C7):
            ref = record.get("gold", {}).get(cand, {}).get("reference", {})
            if ref.get("verdict") != "passed":
                anomalies.append(f"{tid} {cand}: gold suite on reference -> {ref.get('verdict')} {ref.get('failed_tests')}")
        for m in record["mutants"]:
            fam = families.setdefault(m["family"], collections.Counter())
            fam["generated"] += 1
            if m["status"] != "differs":
                row["no_difference"] += 1
                fam["no_difference"] += 1
                continue
            row["applicable"] += 1
            fam["applicable"] += 1
            v6, v7 = verdict(m, C6), verdict(m, C7)
            # A suite that hangs past the per-run timeout does not accept the mutant: count it as killed.
            v6, v7 = ("failed" if v == "timeout" else v for v in (v6, v7))
            for cand, v in ((C6, v6), (C7, v7)):
                if v == "passed":
                    row["gaps"][cand].append(m["id"])
                    fam[f"gap_{cand[-3:]}"] += 1
                elif v not in ("failed", None):
                    anomalies.append(f"{tid} {m['id']} {cand}: {v}")
            for cand in (C6, C7):
                if verdict(m, cand) == "timeout":
                    anomalies.append(f"{tid} {m['id']} {cand}: pytest timeout ({m['gold'][cand].get('seconds')} s; mutant loops forever) - counted as killed")
            entry = {"task": tid, "split": record["split"], "mutant": m["id"], "family": m["family"],
                     "requirement": m["requirement"], "witness": m["witness"]}
            if v6 == "passed" and v7 == "failed":
                row["fixed"].append(m["id"]); fixed_gaps.append(entry); fam["fixed"] += 1
                entry["killed_by_007"] = m["gold"][C7].get("failed_tests")
            elif v6 == "passed" and v7 == "passed":
                row["still_open"].append(m["id"]); open_gaps.append(entry); fam["still_open"] += 1
            elif v6 == "failed" and v7 == "passed":
                row["new_in_007"].append(m["id"]); new_gaps.append(entry); fam["new_in_007"] += 1
        per_task.append(row)

    known = []
    for tid, (label, pick) in KNOWN_BEHAVIOURAL.items():
        if tid not in tasks:
            continue
        ms = [m for m in tasks[tid]["mutants"] if pick(m)]
        known.append({"task": tid, "gap": label, "mutants": [m["id"] for m in ms if m["status"] == "differs"],
                      C6: status_of(ms, C6), C7: status_of(ms, C7)})
    for tid in ORDINARY_16:
        if tid not in tasks:
            continue
        ms = [m for m in tasks[tid]["mutants"] if item_level_ordinary(m, tasks[tid])]
        known.append({"task": tid, "gap": "plain wrong-type list element accepted", "mutants": [m["id"] for m in ms if m["status"] == "differs"],
                      C6: status_of(ms, C6), C7: status_of(ms, C7)})

    summary = {"meta": data["meta"], "families": {k: dict(v) for k, v in families.items()}, "known_gaps": known,
               "per_task": per_task, "still_open": open_gaps, "fixed": fixed_gaps, "new_in_007": new_gaps,
               "anomalies": anomalies,
               "totals": {"tasks": len(tasks), "generated": sum(r["mutants"] for r in per_task),
                          "applicable": sum(r["applicable"] for r in per_task),
                          "gap_006": sum(len(r["gaps"][C6]) for r in per_task),
                          "gap_007": sum(len(r["gaps"][C7]) for r in per_task),
                          "fixed": len(fixed_gaps), "still_open": len(open_gaps), "new_in_007": len(new_gaps),
                          "tasks_with_gap_006": sum(bool(r["gaps"][C6]) for r in per_task),
                          "tasks_with_gap_007": sum(bool(r["gaps"][C7]) for r in per_task)}}
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=1))

    L = ["# Generated tables (make_report.py)", "",
         f"Generated {data['meta']['generated_utc']} from commit `{data['meta']['repo_commit'][:12]}`; "
         f"Python {data['meta']['python']}, pytest {data['meta']['pytest']}. Do not edit by hand.", ""]
    t = summary["totals"]
    L += ["## Totals", "", "| Metric | Value |", "|---|---:|"]
    L += [f"| {k.replace('_', ' ')} | {v} |" for k, v in t.items()]
    L += ["", "## By requirement family", "",
          "| Family | Generated | Differs (applicable) | No difference found | Gaps 006 | Gaps 007 | Fixed | Still open | New in 007 |",
          "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for fam, c in families.items():
        L.append(f"| {fam} | {c['generated']} | {c['applicable']} | {c['no_difference']} | {c['gap_006']} | {c['gap_007']} | {c['fixed']} | {c['still_open']} | {c['new_in_007']} |")
    L += ["", "## Previously reported gaps", "", "| Task | Gap | Mutants | candidate-006 | candidate-007 |", "|---|---|---|---|---|"]
    for k in known:
        L.append(f"| {k['task']} | {k['gap']} | {', '.join(k['mutants']) or '-'} | {k[C6]} | {k[C7]} |")
    L += ["", "## Per task", "", "| Task | Split | Applicable | Gaps 006 | Gaps 007 | Fixed | Still open (007) | New in 007 |", "|---|---|---:|---:|---:|---:|---|---|"]
    for r in per_task:
        L.append(f"| {r['task']} | {r['split'][:3]} | {r['applicable']} | {len(r['gaps'][C6])} | {len(r['gaps'][C7])} | {len(r['fixed'])} | "
                 f"{', '.join(r['still_open']) or '-'} | {', '.join(r['new_in_007']) or '-'} |")
    def gap_rows(title, rows):
        out = ["", f"## {title} ({len(rows)})", "", "| Task | Mutant | Requirement | Witness args | Reference | Mutant |", "|---|---|---|---|---|---|"]
        for g in rows:
            w = g["witness"]
            def show(o):
                return (o["outcome"] + " " + (o["value"] or "")).replace("|", "\\|")[:90] + ("" if o["post_args"] == w["reference"]["post_args"] else f"; args after: {o['post_args']}"[:80])
            out.append(f"| {g['task']} | `{g['mutant']}` | {g['requirement'].replace('|', '/')} | `{w['args_python'][:70]}` | {show(w['reference'])} | {show(w['mutant'])} |")
        return out
    L += gap_rows("Gaps still open in candidate-007", open_gaps)
    L += gap_rows("Gaps new in candidate-007", new_gaps)
    L += gap_rows("Gaps fixed by candidate-007", fixed_gaps)
    L += ["", "## Anomalies", ""] + ([f"- {a}" for a in anomalies] or ["None: every gold suite passed its reference and every applicable mutant run ended in pass/fail without timeout or collection error."])
    (RESULTS / "TABLES.md").write_text("\n".join(L) + "\n")
    print(json.dumps(t))


if __name__ == "__main__":
    main()
