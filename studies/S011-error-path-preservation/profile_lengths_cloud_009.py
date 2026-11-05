"""Tokenizer-only length profile for candidate-009 with the pinned Qwen tokenizer (no weights, no CUDA).

    python studies/S011-error-path-preservation/profile_lengths_cloud_009.py --out <dir>

Same counting method as studies/S007-measurement-repair/profile_repair.py, but the tokenizer is
downloaded from the Hub at the pinned revision instead of the local checkpoint. Calibration gate:
re-profiling candidate-007 must reproduce the committed S007 token-profile.json exactly, row by row,
before candidate-009 numbers are reported.
"""
import argparse, json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
EXP = HERE.parents[1]
BASE = "Qwen/Qwen3.5-9B"
REV = "c202236235762e1c871ad0ccb60c8ee5ba337b9a"


def profile(tok, candidate):
    rows = []
    path = EXP / "dataset-v1" / candidate / "model-packets" / "training-requests.jsonl"
    for line in path.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        text = tok.apply_chat_template(row["messages"], tokenize=False, add_generation_prompt=False, enable_thinking=False)
        length = len(tok(text, add_special_tokens=False)["input_ids"])
        answer = len(tok(row["messages"][-1]["content"], add_special_tokens=False)["input_ids"])
        rows.append(dict(id=row["id"], complete_chat_tokens=length, plain_assistant_text_tokens=answer))
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    out = pathlib.Path(args.out); out.mkdir(parents=True, exist_ok=True)
    import transformers, tokenizers
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(BASE, revision=REV)
    measured = {r["id"]: r for r in json.loads((EXP / "studies/S007-measurement-repair/token-profile.json").read_text())["rows"]}
    again = profile(tok, "candidate-007")
    mismatch = [r["id"] for r in again if measured.get(r["id"]) != r]
    calibration = dict(rows=len(again), mismatched_ids=mismatch, reproduces_s007=not mismatch)
    rows = profile(tok, "candidate-009")
    by7 = {r["id"]: r for r in again}
    report = dict(scope="CPU tokenizer profile only; not loss-mask validation, training export, GPU fit or instruction-following evidence.",
                  tokenizer=dict(repo=BASE, revision=REV, transformers=transformers.__version__, tokenizers=tokenizers.__version__),
                  calibration_against_s007=calibration,
                  maximum_chat_tokens=max(x["complete_chat_tokens"] for x in rows),
                  maximum_plain_answer_tokens=max(x["plain_assistant_text_tokens"] for x in rows),
                  over_previous_2048_chat_budget=[x["id"] for x in rows if x["complete_chat_tokens"] > 2048],
                  total_chat_tokens_007=sum(r["complete_chat_tokens"] for r in again),
                  total_chat_tokens_009=sum(r["complete_chat_tokens"] for r in rows),
                  rows=[r | dict(delta_vs_007=r["complete_chat_tokens"] - by7[r["id"]]["complete_chat_tokens"]) for r in rows])
    overlay = HERE / "tr058-fit-overlay"
    if (overlay / "messages.json").exists():
        import hashlib
        check = json.loads((overlay / "validation.json").read_text(encoding="utf-8"))
        assert hashlib.sha256((overlay / "messages.json").read_bytes()).hexdigest() == check["messages_sha256"]
        messages = json.loads((overlay / "messages.json").read_text(encoding="utf-8"))
        text = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=False, enable_thinking=False)
        tokens = len(tok(text, add_special_tokens=False)["input_ids"])
        others = [r["complete_chat_tokens"] for r in rows if r["id"] != "TR058"]
        report["tr058_fit_overlay"] = dict(messages_sha256=check["messages_sha256"], chat_tokens=tokens,
                                           original_chat_tokens=next(r["complete_chat_tokens"] for r in rows if r["id"] == "TR058"),
                                           within_2048=tokens <= 2048, maximum_full_training_chat_with_overlay=max(others + [tokens]))
    (out / "token-profile-009.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "rows"}, indent=2))
    print("PROFILE_JSON:" + json.dumps(report, separators=(",", ":")))
    if mismatch:
        sys.exit("cloud tokenizer does not reproduce the S007 profile; candidate-009 numbers are not certified")


if __name__ == "__main__":
    main()
