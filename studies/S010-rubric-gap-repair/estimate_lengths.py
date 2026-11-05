"""Estimate candidate-008 training-chat token lengths without the tokenizer (CPU, offline).

The pinned Qwen tokenizer was not reachable from the build environment. Each task's
tokens-per-character ratio for the plain assistant answer and for the complete chat is
taken from the measured candidate-007 profile (studies/S007-measurement-repair/token-profile.json)
and applied to the candidate-008 text. This is an estimate; profile with the pinned tokenizer
before any training use.
"""
import json, pathlib
EXP = pathlib.Path(__file__).resolve().parents[2]
prof = {r["id"]: r for r in json.loads((EXP / "studies/S007-measurement-repair/token-profile.json").read_text())["rows"]}
def packets(c):
    return {p["id"]: p for p in map(json.loads, (EXP / f"dataset-v1/{c}/model-packets/training-requests.jsonl").read_text(encoding="utf-8").splitlines())}
p7, p8 = packets("candidate-007"), packets("candidate-008")
rows = []
for ident, row in sorted(prof.items()):
    a7 = p7[ident]["messages"][-1]["content"]; a8 = p8[ident]["messages"][-1]["content"]
    c7 = sum(len(m["content"]) for m in p7[ident]["messages"]); c8 = sum(len(m["content"]) for m in p8[ident]["messages"])
    ans = round(row["plain_assistant_text_tokens"] * len(a8) / len(a7)); chat = round(row["complete_chat_tokens"] + (ans - row["plain_assistant_text_tokens"]) + (row["complete_chat_tokens"] - row["plain_assistant_text_tokens"]) * ((c8 - len(a8)) / (c7 - len(a7)) - 1))
    rows.append(dict(id=ident, chat_tokens_007=row["complete_chat_tokens"], chat_tokens_008_estimate=chat, delta=chat - row["complete_chat_tokens"]))
changed = [r for r in rows if r["delta"]]
out = dict(method=__doc__.strip(), maximum_007=max(r["chat_tokens_007"] for r in rows), maximum_008_estimate=max(r["chat_tokens_008_estimate"] for r in rows),
           over_2048_007=[r["id"] for r in rows if r["chat_tokens_007"] > 2048], over_2048_008_estimate=[r["id"] for r in rows if r["chat_tokens_008_estimate"] > 2048],
           total_007=sum(r["chat_tokens_007"] for r in rows), total_008_estimate=sum(r["chat_tokens_008_estimate"] for r in rows), changed_tasks=changed)
(pathlib.Path(__file__).parent / "length-estimate.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps({k: v for k, v in out.items() if k not in ("changed_tasks", "method")}, indent=1)); print(sorted(((r["delta"], r["id"]) for r in changed), reverse=True)[:8])
