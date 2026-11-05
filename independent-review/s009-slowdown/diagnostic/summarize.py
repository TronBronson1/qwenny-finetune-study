#!/usr/bin/env python3
"""Summarize one diagnostic run folder and apply the frozen interpretation rules (PROTOCOL.md §5).

    python independent-review/s009-slowdown/diagnostic/summarize.py independent-review/s009-slowdown/diagnostic/runs/<stamp>
"""
import csv, json, pathlib, re, statistics, sys

MIB = 1024 ** 2


def load_events(folder):
    path = folder / "events.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()] if path.exists() else []


def windows_shared_peak(folder, pid):
    path = folder / "windows-gpu-process-memory.csv"
    if not path.exists() or pid is None:
        return None, None
    trainer, others = 0, {}
    with path.open(encoding="utf-8-sig", errors="replace") as f:
        for row in csv.DictReader(f):
            inst, counter = row.get("instance", ""), row.get("counter", "").lower()
            try:
                value = int(row.get("bytes") or 0)
            except ValueError:
                continue
            if re.search(rf"pid_{pid}_", inst) and "shared" in counter:
                trainer = max(trainer, value)
            elif "dedicated" in counter:
                key = re.sub(r"_luid.*", "", inst)
                others[key] = max(others.get(key, 0), value)
    return trainer, sum(others.values())


def condition_row(folder, ledger_entry):
    events = load_events(folder)
    start = next((e for e in events if e["kind"] == "start"), {})
    micro = [e for e in events if e["kind"] == "microbatch"]
    secs = [e["seconds"] for e in micro]
    median = statistics.median(secs) if secs else None
    frees = [e["memory"]["cuda_free"] for e in micro if e.get("memory")]
    reserved = [e["memory"]["reserved"] for e in micro if e.get("memory")]
    total = micro[0]["memory"]["total"] if micro else None
    outside = [total - r - f for r, f in zip(reserved, frees)] if total else []
    shared_peak, other_dedicated = windows_shared_peak(folder, start.get("pid"))
    stall = next((e for e in events if e["kind"] == "watchdog-stop"), None)
    error = next((e for e in events if e["kind"] == "error"), None)
    return dict(
        condition=ledger_entry["condition"], status=ledger_entry["status"], seconds=ledger_entry.get("seconds"),
        microbatches=len(micro), median_s=round(median, 3) if median else None, max_s=round(max(secs), 2) if secs else None,
        slow_over_3x_median=sum(s > 3 * median for s in secs) if median else None,
        min_free_MiB=round(min(frees) / MIB) if frees else None, max_reserved_MiB=round(max(reserved) / MIB) if reserved else None,
        max_outside_reserve_MiB=round(max(outside) / MIB) if outside else None,
        alloc_retries=micro[-1]["memory"].get("num_alloc_retries") if micro else None,
        ooms=micro[-1]["memory"].get("num_ooms") if micro else None,
        trainer_shared_peak_MiB=round(shared_peak / MIB) if shared_peak is not None else None,
        other_processes_dedicated_peak_sum_MiB=round(other_dedicated / MIB) if other_dedicated is not None else None,
        stall=stall and stall.get("reason"), stall_at=stall and stall.get("microbatch"), error=error and error.get("error"))


def success(row):
    return row["status"] == "completed" and row["microbatches"] == 300 and (row["min_free_MiB"] or 0) >= 256


def interpret(rows):
    by = {r["condition"]: r for r in rows}
    c0 = [by[c] for c in ("C0a", "C0b") if c in by]
    if any(r["status"] == "telemetry-invalid" for r in rows):
        return "Some conditions were telemetry-invalid; those conditions carry no evidence. Repair telemetry before interpreting."
    if not c0 or not any(r["status"] in ("watchdog-stall", "ceiling") or (r["min_free_MiB"] is not None and r["min_free_MiB"] < 128) for r in c0):
        return "Controls did not stall: the S009 stall did not reproduce. Mitigation results are uninformative (frozen rule)."
    fixed = [c for c in ("C1", "C2", "C3", "C4", "C5") if c in by and success(by[c])]
    lines = [f"Control stalled. Conditions meeting the success rule (300 microbatches, no watchdog, min free >= 256 MiB): {fixed or 'none'}."]
    if fixed == ["C5"]:
        lines.append("Only C5 succeeded: external GPU consumers are implicated (frozen rule).")
    if "C4" in by and by["C4"]["status"] == "error":
        lines.append("C4 ended with an error under the 0.80 cap (likely OOM): our own demand exceeded the cap; do not raise the cap within this study.")
    return " ".join(lines)


def main():
    root = pathlib.Path(sys.argv[1])
    ledger = json.loads((root / "ledger.json").read_text(encoding="utf-8"))
    rows = [condition_row(root / e["condition"], e) if e["status"] != "skipped-awaiting-user" else dict(condition=e["condition"], status=e["status"])
            for e in ledger["conditions"]]
    summary = dict(dry_run=ledger["dry_run"], protocol_sha256=ledger["protocol_sha256"], conditions=rows, interpretation=interpret([r for r in rows if "microbatches" in r]))
    (root / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    cols = ["condition", "status", "microbatches", "median_s", "max_s", "slow_over_3x_median", "min_free_MiB", "max_outside_reserve_MiB",
            "trainer_shared_peak_MiB", "alloc_retries", "stall_at"]
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    lines += ["| " + " | ".join(str(r.get(c, "")) for c in cols) + " |" for r in rows]
    (root / "SUMMARY.md").write_text("# Diagnostic summary\n\n" + "\n".join(lines) + "\n\n" + summary["interpretation"] + "\n", encoding="utf-8")
    print("\n".join(lines)); print(summary["interpretation"])


if __name__ == "__main__":
    main()
