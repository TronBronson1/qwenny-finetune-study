#!/usr/bin/env python3
"""S009 slowdown forensics from the artifacts committed to this repository.

    python3 independent-review/s009-slowdown/s009_forensics.py
    python3 independent-review/s009-slowdown/s009_forensics.py --run-dir <local training-v1/runs/qwenny-003-calibrated-baseline>

The per-microbatch event log (training-v1/runs/qwenny-003-calibrated-baseline/events.jsonl),
the nvidia-smi samples (gpu-memory.csv) and the Windows counter CSV are git-ignored: only their
SHA-256 values are committed (studies/S009-value-comments/result-sha256.json). Without them, this script
reconstructs the exact microbatch sequence from the frozen shuffle (train_s009.py: random.Random(42+epoch))
and checks it against the logged token totals; time and memory columns stay empty.
With --run-dir, the local files are hash-checked against the committed values and the
per-microbatch time/memory columns are filled from events.jsonl.

Only the standard library plus matplotlib are used. Outputs land next to this file.
"""
import argparse
import csv
import hashlib
import json
import random
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
S009 = REPO / "studies" / "S009-value-comments"
OUT = HERE / "outputs"
FIG = HERE / "figures"
GB = 1e9
MIB = 1024 ** 2
RUN_KEY = "training-v1/runs/qwenny-003-calibrated-baseline/"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def reconstruct_sequence():
    rows = [json.loads(line) for line in (S009 / "preparation-001" / "baseline" / "train.jsonl").read_text(encoding="utf-8").splitlines()]
    sequence = []
    for epoch in range(1, 6):
        order = list(range(len(rows)))
        random.Random(42 + epoch).shuffle(order)  # identical to train_s009.py
        for position, index in enumerate(order, 1):
            r = rows[index]
            sequence.append({"microbatch": len(sequence) + 1, "epoch": epoch, "position": position, "task": r["id"],
                             "input_tokens": r["input_tokens"], "target_tokens": r["target_tokens"],
                             "optimizer_step_in_batch": position % 4 == 0})
    return rows, sequence


def verify_local(run_dir):
    """Hash-check optional local run files against the committed digests."""
    digests = load(S009 / "result-sha256.json")
    found = {}
    for name in ("events.jsonl", "gpu-memory.csv", "windows-process-memory.csv", "windows-monitor.log", "report.json"):
        path = Path(run_dir) / name
        if path.exists():
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            found[name] = {"sha256": actual, "matches_committed": actual == digests.get(RUN_KEY + name)}
    return found


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", help="local copy of training-v1/runs/qwenny-003-calibrated-baseline (optional)")
    args = parser.parse_args()
    OUT.mkdir(exist_ok=True)
    FIG.mkdir(exist_ok=True)

    stopped = load(S009 / "stopped-evidence-001.json")
    execution = load(S009 / "execution-001.json")
    base = stopped["baseline"]
    rows, sequence = reconstruct_sequence()
    logged = base["logged_completed_microbatches"]

    # 1. Reconstruction check against logged totals.
    recon = {
        "logged_microbatches": logged,
        "reconstructed_input_tokens": sum(s["input_tokens"] for s in sequence[:logged]),
        "logged_input_tokens": base["logged_input_tokens"],
        "reconstructed_supervised_tokens": sum(s["target_tokens"] for s in sequence[:logged]),
        "logged_supervised_tokens": base["logged_supervised_tokens"],
        "reconstructed_optimizer_updates": logged // 4,
        "logged_optimizer_updates": base["last_logged_optimizer_updates"],
    }
    recon["exact_match"] = (recon["reconstructed_input_tokens"] == recon["logged_input_tokens"]
                            and recon["reconstructed_supervised_tokens"] == recon["logged_supervised_tokens"]
                            and recon["reconstructed_optimizer_updates"] == recon["logged_optimizer_updates"])
    unfinished = sequence[logged]
    lengths = sorted((r["input_tokens"] for r in rows), reverse=True)
    unfinished["length_rank_of_60"] = lengths.index(unfinished["input_tokens"]) + 1

    # 2. Optional local per-microbatch evidence.
    local = verify_local(args.run_dir) if args.run_dir else {}
    events = []
    if args.run_dir and (Path(args.run_dir) / "events.jsonl").exists():
        events = [json.loads(line) for line in (Path(args.run_dir) / "events.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    micro = [e for e in events if e.get("kind") == "microbatch"]
    for s, e in zip(sequence, micro):
        assert (s["epoch"], s["position"], s["task"]) == (e["epoch"], e["position"], e["id"]), "event/sequence mismatch"
        m = e["memory"]
        s.update(seconds=e["seconds"], allocated=m["allocated"], reserved=m["reserved"], cuda_free=m["cuda_free"],
                 peak_allocated=m["peak_allocated"], peak_reserved=m["peak_reserved"], unix_time=e["unix_time"])
    for i, s in enumerate(sequence):
        s["status"] = "completed (logged)" if i < logged else ("unfinished at 1200 s ceiling" if i == logged else "not reached")
    columns = ["microbatch", "epoch", "position", "task", "input_tokens", "target_tokens", "optimizer_step_in_batch", "status",
               "seconds", "allocated", "reserved", "cuda_free", "peak_allocated", "peak_reserved", "unix_time"]
    with (OUT / "microbatch-table.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, columns)
        writer.writeheader()
        for s in sequence[:logged + 1]:
            writer.writerow({c: s.get(c, "") for c in columns})

    # 3. Device memory accounting at the recorded points.
    total = stopped["preflights"]["baseline"]["full_actual_example_preflight"]["memory"]["total"]
    points = []
    for arm in ("baseline", "comments"):
        m = stopped["preflights"][arm]["full_actual_example_preflight"]["memory"]
        points.append({"point": f"preflight-{arm} (longest example, after backward)", "unix_time": m["unix_time"],
                       "reserved": m["reserved"], "allocated": m["allocated"], "peak_allocated": m["peak_allocated"],
                       "cuda_free": m["cuda_free"], "outside_pytorch_reserved": total - m["reserved"] - m["cuda_free"]})
    points.append({"point": "training, zero-free samples (upper bound on reserved = training peak)",
                   "reserved": base["peak_reserved_bytes"], "cuda_free": 0,
                   "outside_pytorch_reserved_lower_bound": total - base["peak_reserved_bytes"]})
    post_free = 8138 * MIB  # RESULTS.md: post-termination driver query
    guard_free = 8 * 1024 ** 3  # runtime.load_base asserts free >= 8 GiB before loading
    accounting = {
        "total_bytes": total,
        "points": points,
        "post_run_free_bytes": post_free,
        "post_run_other_consumers_bytes": total - post_free,
        "load_guard_free_bytes": guard_free,
        "other_consumers_at_training_load_upper_bound_bytes": total - guard_free,
        "note": ("At load, free >= 8 GiB with this process's CUDA context X already created, so other consumers <= total - 8 GiB - X. "
                 "After termination (no context) other consumers = total - 8138 MiB. Growth >= 54 MiB + X."),
        "growth_between_preflights_bytes": points[1]["outside_pytorch_reserved"] - points[0]["outside_pytorch_reserved"],
        "growth_between_preflights_seconds": points[1]["unix_time"] - points[0]["unix_time"],
    }
    for context_mib in (0, 250, 400, 600):
        accounting[f"min_other_consumer_growth_MiB_if_context_{context_mib}MiB"] = round((total - post_free - (total - guard_free - context_mib * MIB)) / MIB, 1)

    # 4. Wall-time budget of the train-baseline arm.
    pre_seconds = execution["jobs"][0]["seconds"]  # separate preflight process: load + identical pre-training checks
    budget = {
        "arm_ceiling_seconds": 1200,
        "pretraining_phase_estimate_seconds": round(pre_seconds, 1),
        "pretraining_basis": "baseline preflight job wall time (same load/verification/longest-example/smoke/base-dev-loss steps run inside the training process before step 1)",
        "logged_microbatch_seconds": round(base["logged_microbatch_seconds"], 1),
        "checkpoint_eval_estimate_seconds": [30, 90],
        "checkpoint_basis": "two checkpoints (E1, E3): adapter + optimizer save, reload probe and 24 no-grad development losses each; not logged in committed files",
    }
    lo = 1200 - pre_seconds - base["logged_microbatch_seconds"] - budget["checkpoint_eval_estimate_seconds"][1]
    hi = 1200 - pre_seconds - base["logged_microbatch_seconds"] - budget["checkpoint_eval_estimate_seconds"][0]
    budget["unfinished_microbatch_running_seconds_range"] = [round(lo), round(hi)]
    zero_n, pos_n = base["zero_free_samples"], base["positive_free_samples"]
    budget["positive_free_seconds_if_zero_free_sum_is_4x_median"] = round(base["logged_microbatch_seconds"] - zero_n * base["median_batch_seconds_zero_free"], 1)
    mean_pos = budget["positive_free_seconds_if_zero_free_sum_is_4x_median"] / pos_n
    budget["implied_mean_positive_free_seconds"] = round(mean_pos, 3)
    # Projection of the full 5-epoch arm with no slowdown at the observed positive-free pace.
    budget["projected_undisturbed_arm_seconds"] = {
        "at_median_2.672s": round(pre_seconds + 300 * base["median_batch_seconds_positive_free"] + 3 * 30),
        "at_implied_mean": round(pre_seconds + 300 * mean_pos + 3 * 45),
    }
    budget["headroom_fraction_at_median"] = round(1 - budget["projected_undisturbed_arm_seconds"]["at_median_2.672s"] / 1200, 3)

    # 5. Cross-run reference points on the same machine.
    lf = REPO / "lora-feasibility"
    tv = REPO / "training-v1"
    timing = load(lf / "timing-summary.json")
    fit = load(lf / "fit-2048-summary.json")
    real = load(lf / "real-length-summary.json")
    q1 = load(tv / "training-summary.json")
    compact = load(tv / "compact-trial-results.json")["training"]
    refs = [
        {"run": "feasibility seq768 chunk128 (10 synthetic steps)", "median_step_s": timing["median_seconds"], "min_free_MiB": timing["min_stage_free_bytes"] / MIB,
         "peak_reserved_GB": timing["peak_reserved_bytes"] / GB, "windows_peak_shared_MB": timing["windows_training_peak_shared_bytes"] / 1e6, "stalled": False},
        {"run": "feasibility seq768 no chunk (trial-003)", "median_step_s": real[0]["step_seconds"], "min_free_MiB": real[0]["min_stage_free_bytes"] / MIB,
         "peak_reserved_GB": real[0]["peak_reserved_bytes"] / GB, "windows_peak_shared_MB": None, "stalled": False,
         "note": "peak reserved exceeds the 10.74 GB device; completed without OOM but ~20x slower"},
        {"run": "fit-2048 cpu-embed (3 synthetic steps)", "median_step_s": fit["median_step_seconds"], "min_free_MiB": fit["training_min_stage_cuda_free_bytes"] / MIB,
         "peak_reserved_GB": fit["training_peak_reserved_bytes"] / GB, "windows_peak_shared_MB": fit["windows_training_peak_shared_bytes"] / 1e6, "stalled": False},
        {"run": "fit-2048 GPU embedding (interrupted)", "median_step_s": None, "min_free_MiB": 0, "peak_reserved_GB": None,
         "windows_peak_shared_MB": fit["baseline_peak_sampled_process_shared_bytes"] / 1e6, "stalled": True,
         "note": fit["baseline"]["reason"]},
        {"run": "qwenny-001 (300 microbatches, 5 epochs, Nov 3)", "median_step_s": q1["median_microbatch_seconds"], "min_free_MiB": q1["min_microbatch_stage_cuda_free_bytes"] / MIB,
         "peak_reserved_GB": q1["training_peak_reserved_bytes"] / GB, "windows_peak_shared_MB": q1["windows_peak_process_shared_bytes_during_training_interval"] / 1e6,
         "stalled": False, "note": f"completed in {q1['elapsed_training_and_checkpoint_evaluation_seconds']:.0f} s incl. 3 checkpoint evaluations; max example 1954 tokens"},
        {"run": "qwenny-002 compact (Nov 3/4)", "median_step_s": None, "min_free_MiB": compact["min_stage_cuda_free_bytes"] / MIB,
         "peak_reserved_GB": compact["training_peak_reserved_bytes"] / GB, "windows_peak_shared_MB": compact["windows_peak_shared_bytes"] / 1e6, "stalled": False,
         "note": f"completed in {compact['elapsed_training_and_checkpoint_evaluation_seconds']:.0f} s"},
        {"run": "S009 baseline, positive-free samples (Nov 4)", "median_step_s": base["median_batch_seconds_positive_free"], "min_free_MiB": None,
         "peak_reserved_GB": base["peak_reserved_bytes"] / GB, "windows_peak_shared_MB": None, "stalled": False, "note": f"{pos_n} samples"},
        {"run": "S009 baseline, zero-free samples", "median_step_s": base["median_batch_seconds_zero_free"], "min_free_MiB": 0,
         "peak_reserved_GB": base["peak_reserved_bytes"] / GB, "windows_peak_shared_MB": None, "stalled": True, "note": f"{zero_n} samples, then an unfinished batch"},
    ]

    analysis = {"reconstruction": recon, "unfinished_microbatch": unfinished, "memory_accounting": accounting,
                "time_budget": budget, "reference_runs": refs, "local_run_files": local,
                "per_microbatch_time_memory_available": bool(micro),
                "longest_examples": sorted(({"task": r["id"], "input_tokens": r["input_tokens"]} for r in rows), key=lambda x: -x["input_tokens"])[:5],
                "longest_example_occurrences_before_stop": [{"task": s["task"], "microbatch": s["microbatch"], "epoch": s["epoch"]}
                                                           for s in sequence[:logged] if s["input_tokens"] >= 1800]}
    (OUT / "analysis.json").write_text(json.dumps(analysis, indent=1), encoding="utf-8")
    plots(sequence, logged, analysis, total)
    print(json.dumps({"reconstruction_exact": recon["exact_match"], "unfinished": unfinished, "time_budget": budget}, indent=1))


def plots(sequence, logged, analysis, total):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    shown = sequence[:logged + 1]
    fig, ax = plt.subplots(figsize=(11, 4))
    colors = plt.cm.tab10.colors
    for epoch in range(1, 5):
        pts = [s for s in shown if s["epoch"] == epoch]
        ax.bar([s["microbatch"] for s in pts], [s["input_tokens"] for s in pts], color=colors[epoch - 1], width=0.9, label=f"epoch {epoch}")
    u = shown[-1]
    ax.bar([u["microbatch"]], [u["input_tokens"]], color="red", width=2.5, label=f"unfinished: {u['task']} ({u['input_tokens']} tok)")
    for boundary, label in ((60.5, "E1 checkpoint + 24 dev losses"), (180.5, "E3 checkpoint + 24 dev losses")):
        ax.axvline(boundary, color="k", ls="--", lw=1)
        ax.text(boundary + 1, 1950, label, fontsize=8, va="top")
    if any("seconds" in s for s in shown):
        ax2 = ax.twinx()
        ax2.plot([s["microbatch"] for s in shown if "seconds" in s], [s["seconds"] for s in shown if "seconds" in s], "k.", ms=3)
        ax2.set_ylabel("seconds"); ax2.set_yscale("log")
    ax.set_xlabel("microbatch (reconstructed order; matches logged token totals exactly)")
    ax.set_ylabel("input tokens")
    ax.set_title("S009 baseline arm: sequence length of every microbatch up to the stop")
    ax.legend(fontsize=7, ncol=3, loc="lower right")
    fig.tight_layout(); fig.savefig(FIG / "microbatch_lengths.png", dpi=150); plt.close(fig)

    acc = analysis["memory_accounting"]
    labels, reserved, outside, free = [], [], [], []
    for p in acc["points"][:2]:
        labels.append(p["point"].split(" (")[0]); reserved.append(p["reserved"] / GB); outside.append(p["outside_pytorch_reserved"] / GB); free.append(p["cuda_free"] / GB)
    labels.append("training zero-free\n(reserved <= peak)")
    reserved.append(acc["points"][2]["reserved"] / GB); outside.append(acc["points"][2]["outside_pytorch_reserved_lower_bound"] / GB); free.append(0)
    labels.append("post-run\n(no training process)")
    reserved.append(0); outside.append(acc["post_run_other_consumers_bytes"] / GB); free.append(acc["post_run_free_bytes"] / GB)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    x = range(len(labels))
    ax.bar(x, reserved, color="#4c72b0", label="PyTorch reserved (this process)")
    ax.bar(x, outside, bottom=reserved, color="#dd8452", label="outside PyTorch reserve: CUDA context + other processes")
    ax.bar(x, free, bottom=[a + b for a, b in zip(reserved, outside)], color="#55a868", label="reported free")
    ax.axhline(total / GB, color="k", lw=1)
    for i, (r, o, f) in enumerate(zip(reserved, outside, free)):
        ax.text(i, r + o / 2, f"{o:.2f}", ha="center", fontsize=8, color="white")
        ax.text(i, r + o + f + 0.05, f"free {f:.2f}", ha="center", fontsize=8)
    ax.set_xticks(list(x)); ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("GB (10^9 bytes)"); ax.set_ylim(0, 11.5)
    ax.set_title("Device memory accounting (10.74 GB RTX 3080)")
    ax.legend(fontsize=7, loc="lower left")
    fig.tight_layout(); fig.savefig(FIG / "memory_accounting.png", dpi=150); plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    for ref in analysis["reference_runs"]:
        if ref["median_step_s"] is None or ref["min_free_MiB"] is None:
            continue
        ax.scatter(ref["min_free_MiB"], ref["median_step_s"], s=60, color="red" if ref["min_free_MiB"] == 0 else "#4c72b0")
        ax.annotate(ref["run"], (ref["min_free_MiB"], ref["median_step_s"]), fontsize=7, xytext=(5, 3), textcoords="offset points")
    ax.set_yscale("log"); ax.set_xlabel("minimum reported CUDA free memory (MiB)"); ax.set_ylabel("median step / microbatch seconds")
    ax.set_title("Same machine: step time collapses only when free memory reaches zero")
    fig.tight_layout(); fig.savefig(FIG / "free_vs_step_time.png", dpi=150); plt.close(fig)

    b = analysis["time_budget"]
    lo, hi = b["unfinished_microbatch_running_seconds_range"]
    pieces = [("pre-training phase\n(≈ preflight job)", b["pretraining_phase_estimate_seconds"]),
              ("209 positive-free\nmicrobatches", b["positive_free_seconds_if_zero_free_sum_is_4x_median"]),
              ("E1+E3\ncheckpoints\n(est. 30-90)", 60),
              ("4 zero-free\nmicro-\nbatches", b["logged_microbatch_seconds"] - b["positive_free_seconds_if_zero_free_sum_is_4x_median"]), ("unfinished batch\n(est.)", 1200 - b["pretraining_phase_estimate_seconds"] - b["logged_microbatch_seconds"] - 60)]
    fig, ax = plt.subplots(figsize=(11, 3.2))
    left = 0
    for (label, width), color in zip(pieces, ["#8172b3", "#4c72b0", "#c44e52", "#937860", "#ff0000"]):
        ax.barh(0, width, left=left, color=color)
        ax.text(left + width / 2, 0, f"{label}\n{width:.0f} s", ha="center", va="center", fontsize=7, color="white")
        left += width
    ax.axvline(1200, color="k"); ax.set_xlim(0, 1250); ax.set_yticks([])
    ax.set_xlabel("seconds since train-baseline start (1200 s ceiling); segment order is schematic, not a measured timeline")
    ax.set_title(f"Where the 1200 s went (unfinished batch ran ~{lo}-{hi} s; normal ≈ 3 s)")
    fig.tight_layout(); fig.savefig(FIG / "time_budget.png", dpi=150); plt.close(fig)


if __name__ == "__main__":
    main()
