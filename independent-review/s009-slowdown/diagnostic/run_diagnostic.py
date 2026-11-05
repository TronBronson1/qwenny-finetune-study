#!/usr/bin/env python3
"""Frozen local S009 resource diagnostic (see PROTOCOL.md next to this file).

On the training PC, from the repository root, inside the existing lora-feasibility venv:

    python independent-review/s009-slowdown/diagnostic/run_diagnostic.py                  # C0a C1 C2 C3 C4 C0b (C5 skipped)
    python independent-review/s009-slowdown/diagnostic/run_diagnostic.py --c5-confirmed   # include C5 after YOU closed apps
    python independent-review/s009-slowdown/diagnostic/run_diagnostic.py --dry-run --ceiling 60 --idle 1   # CPU-only rehearsal

Each condition runs in a fresh child process that repeats the S009 baseline workload (60 examples,
5 epochs, batch 1 x accumulation 4, rank-4 LoRA, CPU embedding, chunked loss, checkpoints + 24
development losses after epochs 1/3/5) with exactly one change. Checkpoints are written to a
temporary folder and deleted; nothing here is a study endpoint. No existing file is modified.
"""
import argparse, csv, gc, json, os, pathlib, random, re, shutil, statistics, subprocess, sys, tempfile, threading, time

HERE = pathlib.Path(__file__).resolve().parent
EXP = HERE.parents[2]
PACKET = EXP / "studies" / "S009-value-comments" / "preparation-001" / "baseline"
SEQUENCE = ["C0a", "C1", "C2", "C3", "C4", "C5", "C0b"]
CONDITIONS = {
    "C0a": "control: S009 settings",
    "C1": "PYTORCH_CUDA_ALLOC_CONF=garbage_collection_threshold:0.8,max_split_size_mb:256",
    "C2": "length-descending order within each epoch",
    "C3": "gc.collect() + torch.cuda.empty_cache() after each checkpoint and development evaluation",
    "C4": "torch.cuda.set_per_process_memory_fraction(0.80)",
    "C5": "user closed/unloaded approved GPU apps before the run (agent closes nothing)",
    "C0b": "control repeated last (drift bracket)",
}
ALLOC_CONF = "garbage_collection_threshold:0.8,max_split_size_mb:256"
STALL_MIN_SECONDS, STALL_FACTOR, LOW_FREE_BYTES, LOW_FREE_SECONDS = 30.0, 10.0, 128 * 1024 ** 2, 30.0
CHECKPOINT_LIMIT_SECONDS = 300.0  # save + reload probe + 24 no-grad development losses
EXIT_STALL, EXIT_TELEMETRY = 3, 4


def now():
    return time.time()


def jsonl(path, **row):
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(dict(unix_time=now(), **row)) + "\n")


def nvidia_snapshot():
    """Device and per-process GPU memory via nvidia-smi; empty dict when unavailable."""
    out = {}
    try:
        dev = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,memory.free,memory.total", "--format=csv,noheader,nounits"],
                             capture_output=True, text=True, timeout=10).stdout.strip()
        used, free, total = (int(x) for x in dev.splitlines()[0].split(","))
        out.update(used_MiB=used, free_MiB=free, total_MiB=total)
        apps = subprocess.run(["nvidia-smi", "--query-compute-apps=pid,process_name,used_memory", "--format=csv,noheader,nounits"],
                              capture_output=True, text=True, timeout=10).stdout.strip()
        out["compute_apps"] = [dict(zip(("pid", "name", "used_MiB"), (x.strip() for x in line.split(",")))) for line in apps.splitlines() if line.strip()]
    except (OSError, subprocess.SubprocessError, ValueError, IndexError):
        pass
    return out


# ---------------------------------------------------------------------------
class Telemetry:
    """0.5 s nvidia-smi sampling plus Windows GPU Process Memory counters for ALL processes."""
    PS = r'''
$ErrorActionPreference = 'Continue'
'timestamp_utc,instance,counter,bytes' | Set-Content -LiteralPath $args[0] -Encoding utf8
while ($true) {
  $s = Get-Counter -Counter '\GPU Process Memory(*)\Dedicated Usage','\GPU Process Memory(*)\Shared Usage' -MaxSamples 1 -ErrorAction SilentlyContinue
  $t = Get-Date -AsUTC -Format o
  foreach ($c in $s.CounterSamples) { "$t,$($c.InstanceName),$(Split-Path $c.Path -Leaf),$([long]$c.CookedValue)" | Add-Content -LiteralPath $args[0] -Encoding utf8 }
  Start-Sleep -Milliseconds 500
}
'''

    def __init__(self, out, windows):
        self.out, self.windows, self.stop = out, windows, threading.Event()
        self.counter_csv = out / "windows-gpu-process-memory.csv"
        self.proc = None
        if windows:
            script = out / "counters.ps1"; script.write_text(self.PS, encoding="utf-8")
            shell = shutil.which("pwsh") or shutil.which("powershell")
            self.proc = subprocess.Popen([shell, "-NoProfile", "-NonInteractive", "-File", str(script), str(self.counter_csv)],
                                         stdout=subprocess.DEVNULL, stderr=(out / "counters.err").open("w"))
        self.thread = threading.Thread(target=self._sample, daemon=True); self.thread.start()

    def _sample(self):
        path = self.out / "nvidia-smi.jsonl"
        while not self.stop.is_set():
            snap = nvidia_snapshot()
            if snap:
                jsonl(path, **snap)
            self.stop.wait(0.5)

    def trainer_rows(self, pid):
        if not self.counter_csv.exists():
            return 0
        pattern = re.compile(rf"pid_{pid}_")
        with self.counter_csv.open(encoding="utf-8-sig", errors="replace") as f:
            return sum(1 for row in csv.DictReader(f) if pattern.search(row.get("instance", "")))

    def close(self):
        self.stop.set(); self.thread.join(timeout=5)
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()


class Watchdog:
    """Ends the condition on a stalled microbatch or sustained near-zero free memory."""

    def __init__(self, out, free_reader, on_trip):
        self.out, self.free_reader, self.on_trip = out, free_reader, on_trip
        self.started, self.times, self.low_since, self.label, self.fixed = None, [], None, None, None
        threading.Thread(target=self._run, daemon=True).start()

    def begin(self, label, fixed_limit=None):
        self.label, self.fixed, self.started = label, fixed_limit, now()

    def end(self, seconds=None):
        if seconds is not None:
            self.times.append(seconds)
        self.started = None

    def limit(self):
        if self.fixed is not None:
            return self.fixed
        recent = self.times[-20:]
        return max(STALL_MIN_SECONDS, STALL_FACTOR * statistics.median(recent)) if recent else STALL_MIN_SECONDS * 4

    def _trip(self, reason, **details):
        (self.out / "stall.json").write_text(json.dumps(dict(reason=reason, microbatch=self.label, unix_time=now(), **details), indent=2))
        jsonl(self.out / "events.jsonl", kind="watchdog-stop", reason=reason, microbatch=self.label, **details)
        try:
            self.on_trip()
        finally:
            os._exit(EXIT_STALL)

    def _run(self):
        while True:
            time.sleep(1.0)
            if self.started is not None and now() - self.started > self.limit():
                self._trip("microbatch-exceeded-limit", elapsed=now() - self.started, limit=self.limit())
            free = self.free_reader()
            if free is not None and free < LOW_FREE_BYTES:
                self.low_since = self.low_since or now()
                if now() - self.low_since > LOW_FREE_SECONDS:
                    self._trip("free-memory-below-128MiB-for-30s", free_bytes=free)
            else:
                self.low_since = None


# ---------------------------------------------------------------------------
class DryBackend:
    """CPU-only stand-in used to rehearse orchestration, telemetry handling and the watchdog."""

    def __init__(self, condition, inject_stall_at):
        self.condition, self.inject = condition, inject_stall_at
        self.count = 0

    def free_bytes(self):
        return 2 * 1024 ** 3

    def memory(self):
        return dict(allocated=0, reserved=0, peak_allocated=0, peak_reserved=0, cuda_free=self.free_bytes(), total=10 * 1024 ** 3,
                    num_alloc_retries=0, num_ooms=0)

    def setup(self):
        pass

    def train_step(self, record, step_optimizer):
        self.count += 1
        time.sleep(0.002 + record["input_tokens"] * 0.000002)
        if self.inject and self.count == self.inject:
            time.sleep(10 ** 6)  # simulated hang; the watchdog must end the process
        return 1.0

    def checkpoint(self, epoch, dev, folder):
        time.sleep(0.01)

    def after_checkpoint(self):
        pass


class RealBackend:
    """Same objective, optimizer and loop as studies/S009-value-comments/train_s009.py."""

    def __init__(self, condition):
        sys.path.insert(0, str(EXP / "training-v1"))
        import torch  # noqa: F401
        import runtime  # training-v1/runtime.py (unchanged)
        self.torch, self.rt, self.condition = torch, runtime, condition

    def free_bytes(self):
        try:
            return self.torch.cuda.mem_get_info()[0]
        except Exception:  # noqa: BLE001 - telemetry must never crash training
            return None

    def memory(self):
        m = self.rt.memory(); stats = self.torch.cuda.memory_stats()
        m.update(num_alloc_retries=stats.get("num_alloc_retries", 0), num_ooms=stats.get("num_ooms", 0))
        return m

    def setup(self):
        torch, rt = self.torch, self.rt
        if self.condition == "C4":
            torch.cuda.set_per_process_memory_fraction(0.80)
        rt.verify_checkpoint()
        random.seed(42); torch.manual_seed(42); torch.cuda.manual_seed_all(42)
        self.model, self.params, _ = rt.attach_lora(rt.load_base(training=True))
        assert self.model.get_input_embeddings().weight.device.type == "cpu"
        random.seed(42); torch.manual_seed(42); torch.cuda.manual_seed_all(42)
        torch.cuda.reset_peak_memory_stats()
        self.optimizer = torch.optim.AdamW(self.params.values(), lr=1e-4, betas=(.9, .999), eps=1e-8, weight_decay=.01)
        self.optimizer.zero_grad(set_to_none=True); self.updates = 0
        self.model.train()

    def train_step(self, record, step_optimizer):
        torch, rt = self.torch, self.rt
        ids, attention, labels = rt.tensors(record)
        with torch.autocast("cuda", dtype=torch.bfloat16):
            loss = rt.masked_loss(self.model, ids, attention, labels)
        assert torch.isfinite(loss)
        raw = loss.item(); (loss / 4).backward()
        if step_optimizer:
            torch.nn.utils.clip_grad_norm_(list(self.params.values()), 1.0, error_if_nonfinite=True)
            self.updates += 1
            for group in self.optimizer.param_groups:
                group["lr"] = 1e-4 * min(1., self.updates / 3)
            self.optimizer.step(); self.optimizer.zero_grad(set_to_none=True)
        torch.cuda.synchronize()
        del ids, attention, labels, loss
        return raw

    def checkpoint(self, epoch, dev, folder):
        torch, rt = self.torch, self.rt
        self.model.save_pretrained(folder / f"epoch-{epoch}", safe_serialization=True)
        torch.save({"optimizer": self.optimizer.state_dict()}, folder / f"epoch-{epoch}" / "training-state.pt")
        self.model.eval()
        with torch.no_grad():
            for record in dev:
                ids, attention, labels = rt.tensors(record)
                with torch.autocast("cuda", dtype=torch.bfloat16):
                    loss = rt.masked_loss(self.model, ids, attention, labels)
                assert torch.isfinite(loss)
                del ids, attention, labels, loss
        self.model.train()

    def after_checkpoint(self):
        if self.condition == "C3":
            gc.collect(); self.torch.cuda.empty_cache()


# ---------------------------------------------------------------------------
def child(args):
    out = pathlib.Path(args.out); out.mkdir(parents=True, exist_ok=False)
    events = out / "events.jsonl"
    windows = os.name == "nt" and not args.dry_run
    jsonl(events, kind="start", condition=args.condition, description=CONDITIONS[args.condition], pid=os.getpid(),
          alloc_conf=os.environ.get("PYTORCH_CUDA_ALLOC_CONF"), dry_run=args.dry_run, nvidia=nvidia_snapshot())
    backend = DryBackend(args.condition, args.inject_stall_at) if args.dry_run else RealBackend(args.condition)
    telemetry = Telemetry(out, windows)
    try:
        if windows:  # startup telemetry gate: counters must see this trainer process
            deadline = now() + 60
            while telemetry.trainer_rows(os.getpid()) < 10 and now() < deadline:
                time.sleep(2)
            rows = telemetry.trainer_rows(os.getpid())
            jsonl(events, kind="telemetry-check", trainer_counter_rows=rows)
            if rows < 10:
                jsonl(events, kind="telemetry-invalid", trainer_counter_rows=rows)
                return EXIT_TELEMETRY
        else:
            jsonl(events, kind="telemetry-check", windows_counters="not-applicable (non-Windows or dry run)")
        backend.setup()
        jsonl(events, kind="loaded", memory=backend.memory())
        train = [json.loads(line) for line in (PACKET / "train.jsonl").read_text(encoding="utf-8").splitlines()]
        dev = [json.loads(line) for line in (PACKET / "development.jsonl").read_text(encoding="utf-8").splitlines()]
        assert len(train) == 60 and len(dev) == 24
        watchdog = Watchdog(out, backend.free_bytes, telemetry.close)
        scratch = pathlib.Path(tempfile.mkdtemp(prefix="s009diag-ckpt-"))
        index = 0
        try:
            for epoch in range(1, 6):
                order = list(range(len(train))); random.Random(42 + epoch).shuffle(order)
                if args.condition == "C2":
                    order.sort(key=lambda i: -train[i]["input_tokens"])
                for position, i in enumerate(order, 1):
                    index += 1
                    record = train[i]
                    watchdog.begin(f"{epoch}:{position}:{record['id']}")
                    tick = time.monotonic()
                    loss = backend.train_step(record, position % 4 == 0)
                    seconds = time.monotonic() - tick
                    watchdog.end(seconds)
                    jsonl(events, kind="microbatch", index=index, epoch=epoch, position=position, id=record["id"],
                          tokens=record["input_tokens"], target_tokens=record["target_tokens"], loss=loss, seconds=seconds, memory=backend.memory())
                if epoch in (1, 3, 5):
                    tick = time.monotonic(); watchdog.begin(f"checkpoint-{epoch}", CHECKPOINT_LIMIT_SECONDS)
                    jsonl(events, kind="checkpoint-start", epoch=epoch, memory=backend.memory())
                    backend.checkpoint(epoch, dev, scratch)
                    backend.after_checkpoint()
                    watchdog.end()
                    jsonl(events, kind="checkpoint-end", epoch=epoch, seconds=time.monotonic() - tick, memory=backend.memory())
        finally:
            shutil.rmtree(scratch, ignore_errors=True)
        jsonl(events, kind="completed", microbatches=index, memory=backend.memory(), nvidia=nvidia_snapshot())
        return 0
    except Exception as error:  # an OOM under C4 is an expected, recorded outcome
        jsonl(events, kind="error", error=repr(error)[:2000])
        return 2
    finally:
        telemetry.close()


def orchestrate(args):
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    root = HERE / "runs" / (stamp + ("-dry" if args.dry_run else ""))
    root.mkdir(parents=True, exist_ok=False)
    sequence = args.only or SEQUENCE
    ledger = dict(protocol_sha256=__import__("hashlib").sha256((HERE / "PROTOCOL.md").read_bytes()).hexdigest(),
                  script_sha256=__import__("hashlib").sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
                  started_utc=stamp, dry_run=args.dry_run, ceiling_seconds=args.ceiling, conditions=[])
    for position, condition in enumerate(sequence):
        if position:
            time.sleep(args.idle)
        entry = dict(condition=condition, description=CONDITIONS[condition], before=nvidia_snapshot())
        if condition == "C5" and not args.c5_confirmed:
            entry.update(status="skipped-awaiting-user", note="Rerun with --only C5 --c5-confirmed after you close or unload approved GPU apps.")
            ledger["conditions"].append(entry); continue
        env = {k: v for k, v in os.environ.items() if k != "PYTORCH_CUDA_ALLOC_CONF"}
        if condition == "C1":
            env["PYTORCH_CUDA_ALLOC_CONF"] = ALLOC_CONF
        cmd = [sys.executable, str(pathlib.Path(__file__).resolve()), "--child", "--condition", condition, "--out", str(root / condition)]
        if args.dry_run:
            cmd += ["--dry-run"] + (["--inject-stall-at", str(args.inject_stall_at)] if args.inject_stall_at and condition == "C3" else [])
        start = now()
        try:
            code = subprocess.run(cmd, env=env, timeout=args.ceiling).returncode
            status = {0: "completed", EXIT_STALL: "watchdog-stall", EXIT_TELEMETRY: "telemetry-invalid", 2: "error"}.get(code, f"exit-{code}")
        except subprocess.TimeoutExpired:
            code, status = None, "ceiling"
        entry.update(status=status, exit_code=code, seconds=round(now() - start, 1), after=nvidia_snapshot())
        ledger["conditions"].append(entry)
        (root / "ledger.json").write_text(json.dumps(ledger, indent=2))
        print(f"[{condition}] {status} in {entry['seconds']} s", flush=True)
    (root / "ledger.json").write_text(json.dumps(ledger, indent=2))
    subprocess.run([sys.executable, str(HERE / "summarize.py"), str(root)], check=False)
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--child", action="store_true", help=argparse.SUPPRESS)
    p.add_argument("--condition", choices=list(CONDITIONS), help=argparse.SUPPRESS)
    p.add_argument("--out", help=argparse.SUPPRESS)
    p.add_argument("--only", nargs="+", choices=list(CONDITIONS), help="run a subset (default: full frozen sequence)")
    p.add_argument("--c5-confirmed", action="store_true", help="you have closed/unloaded approved GPU apps for C5")
    p.add_argument("--ceiling", type=float, default=1800, help="per-condition wall ceiling in seconds (frozen: 1800)")
    p.add_argument("--idle", type=float, default=120, help="idle gap between conditions in seconds (frozen: 120)")
    p.add_argument("--dry-run", action="store_true", help="CPU-only rehearsal without torch or a GPU")
    p.add_argument("--inject-stall-at", type=int, default=0, help=argparse.SUPPRESS)
    args = p.parse_args()
    sys.exit(child(args) if args.child else orchestrate(args))


if __name__ == "__main__":
    main()
