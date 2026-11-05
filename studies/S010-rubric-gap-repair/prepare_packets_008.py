"""Staged candidate-008 training/development token packets (S009 baseline format). NOT a training authorization.

    python studies/S010-rubric-gap-repair/prepare_packets_008.py            # local pinned checkpoint if present, else the Hub
    python studies/S010-rubric-gap-repair/prepare_packets_008.py --hub      # force the Hub at the pinned revision

Gates, all required before anything is written:
  1. candidate-008 files match SHA256.json, and that hash equals the user-approved hash
     (dataset-v1/USER_REVIEW_2026-11-05.json);
  2. tokenizer calibration: rebuilding the committed S009 baseline packets from candidate-007 with the same
     code reproduces studies/S009-value-comments/preparation-001/baseline/{messages,train,development}.jsonl
     byte-for-byte;
  3. candidate-008 packets apply only the S009 shared presentation changes: the validated S010 TR058 fit
     overlay, TR049 ", " compaction with an exact AST check, and the DV008 accent escape; every executable
     AST equals the candidate-008 gold ignoring display ids;
  4. encode_answer (training-v1/prepare_data.py, unchanged) is applied with the 2,048-token train limit: exact
     answer-only masks, no truncation, decoded supervised text equals each answer.
Output: studies/S010-rubric-gap-repair/packets-008/ (refuses to overwrite).
"""
import argparse, ast, copy, hashlib, json, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
EXP = HERE.parents[1]
C7, C8 = EXP / "dataset-v1/candidate-007", EXP / "dataset-v1/candidate-008"
S009 = EXP / "studies/S009-value-comments/preparation-001/baseline"
OUT = HERE / "packets-008"
APPROVED = "b65935295c94814fc7744f70feac49aedf809847a629961ae9bfbc75f72e18f4"
sys.path.insert(0, str(EXP / "training-v1"))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rows(p):
    return [json.loads(s) for s in p.read_text(encoding="utf-8").splitlines()]


def jsonl(records):
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records)


def code(answer):
    blocks = re.findall(r"```python\s*\n(.*?)```", answer, re.S)
    assert len(blocks) == 1
    return blocks[0]


def normalized(source):
    tree = ast.parse(source)
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name) \
                and n.func.value.id == "pytest" and n.func.attr == "param":
            n.keywords = [k for k in n.keywords if k.arg != "id"]
    return ast.dump(tree, include_attributes=False)


def shared_presentation(records, overlay_messages):
    """S009's shared changes: TR058 overlay and TR049 comma compaction (exact AST)."""
    out = copy.deepcopy(records)
    assert [r["id"] for r in out] == [f"TR{i:03}" for i in range(1, 61)]
    out[57]["messages"] = overlay_messages
    grid = out[48]["messages"][-1]["content"]; grid_code = code(grid)
    compact = re.sub(r", +", ",", grid_code)
    assert ast.dump(ast.parse(grid_code)) == ast.dump(ast.parse(compact))
    out[48]["messages"][-1]["content"] = grid.replace(grid_code, compact, 1)
    return out


def development(tok, encode_answer, candidate):
    demos = []
    for ident in ("D01", "D02"):
        folder = EXP / "prompt-comparison/demonstrations" / ident
        demos += [dict(role="user", content=(folder / "SPEC.md").read_text(encoding="utf-8").strip()),
                  dict(role="assistant", content=(folder / "ANSWER.md").read_text(encoding="utf-8").strip())]
    result = []
    for request in rows(candidate / "model-packets/development-requests.jsonl"):
        ident = request["id"]; assert re.fullmatch(r"DV\d{3}", ident)
        target = (candidate / "tasks/development" / ident / "TARGET.md").read_text(encoding="utf-8")
        if ident == "DV008":
            escaped = target.replace(chr(0x301), "\\u" + "0301")  # literal backslash-u0301, as in S009
            assert ast.dump(ast.parse(code(target))) == ast.dump(ast.parse(code(escaped)))
            target = escaped
        for view in ("A", "B"):
            messages = request["messages"] if view == "A" else [request["messages"][0]] + demos + request["messages"][1:]
            record = encode_answer(tok, messages + [dict(role="assistant", content=target)], ident + "-" + view, 16134)
            record.update(task_id=ident, arm=view); result.append(record)
    assert len(result) == 24
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hub", action="store_true", help="load the tokenizer from the Hub at the pinned revision")
    args = parser.parse_args()
    assert not OUT.exists(), "refuse to overwrite packets-008"
    # Gate 1: approved, unchanged candidate.
    for name, digest in json.loads((C8 / "SHA256.json").read_text(encoding="utf-8")).items():
        assert sha(C8 / name) == digest, name
    approval = json.loads((EXP / "dataset-v1/USER_REVIEW_2026-11-05.json").read_text(encoding="utf-8"))
    assert sha(C8 / "SHA256.json") == APPROVED == approval["dataset_hash_manifest_sha256"] and approval["hash_approved"]
    from prepare_data import encode_answer, CHECKPOINT, REV
    from transformers import AutoTokenizer
    if not args.hub and CHECKPOINT.exists():
        tok, source = AutoTokenizer.from_pretrained(CHECKPOINT, local_files_only=True), "local pinned checkpoint"
    else:
        tok, source = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-9B", revision=REV), f"Hub Qwen/Qwen3.5-9B@{REV}"
    # Gate 2: reproduce committed S009 baseline packets from candidate-007.
    s007_overlay = json.loads((EXP / "studies/S007-measurement-repair/length-preview-002/messages.json").read_text(encoding="utf-8"))
    base7 = shared_presentation(rows(C7 / "model-packets/training-requests.jsonl"), s007_overlay)
    calibration = {
        "messages.jsonl": jsonl(base7) == (S009 / "messages.jsonl").read_text(encoding="utf-8"),
        "train.jsonl": jsonl([encode_answer(tok, r["messages"], r["id"], 2048) for r in base7]) == (S009 / "train.jsonl").read_text(encoding="utf-8"),
        "development.jsonl": jsonl(development(tok, encode_answer, C7)) == (S009 / "development.jsonl").read_text(encoding="utf-8"),
    }
    print("calibration against committed S009 baseline packets:", calibration, flush=True)
    assert all(calibration.values()), "tokenizer/code does not reproduce the S009 baseline packets"
    # Gate 3: candidate-008 records with the validated S010 overlay.
    overlay_path = HERE / "tr058-fit-overlay/messages.json"
    fit = json.loads((HERE / "TRAINING_FIT_OVERLAY.json").read_text(encoding="utf-8"))
    assert sha(overlay_path) == fit["replacement_sha256"] and fit["parent_sha256"] == APPROVED
    base8 = shared_presentation(rows(C8 / "model-packets/training-requests.jsonl"), json.loads(overlay_path.read_text(encoding="utf-8")))
    provenance = []
    for record, parent in zip(base8, rows(C8 / "model-packets/training-requests.jsonl")):
        gold = (C8 / "tasks/training" / record["id"] / "test_target.py").read_text(encoding="utf-8")
        assert normalized(code(record["messages"][-1]["content"])) == normalized(gold), record["id"]
        assert record["messages"][:-1] == parent["messages"][:-1]
        provenance.append(dict(id=record["id"], changed=record != parent, change=("TR058 S010 fit overlay" if record["id"] == "TR058" else
                               "TR049 comma compaction (exact AST)" if record["id"] == "TR049" else None), executable_ast_equal_ignoring_display_ids=True))
    # Gate 4: exact answer-only encoding.
    train = [encode_answer(tok, r["messages"], r["id"], 2048) for r in base8]
    dev = development(tok, encode_answer, C8)
    OUT.mkdir()
    (OUT / "messages.jsonl").write_text(jsonl(base8), encoding="utf-8")
    (OUT / "train.jsonl").write_text(jsonl(train), encoding="utf-8")
    (OUT / "development.jsonl").write_text(jsonl(dev), encoding="utf-8")
    (OUT / "record-provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    for r in (train[0], max(train, key=lambda r: r["input_tokens"])):
        (OUT / (r["id"] + "-mask-review.txt")).write_text("MASKED PREFIX:\n" + tok.decode(r["input_ids"][:r["first_target_token"]], skip_special_tokens=False)
                                                       + "\nSUPERVISED:\n" + tok.decode([v for v in r["labels"] if v != -100], skip_special_tokens=False), encoding="utf-8")
    report = dict(status="staged-not-authorized", candidate="candidate-008", candidate_manifest_sha256=APPROVED, tokenizer_source=source, base_revision=REV,
                  calibration_reproduces_s009_baseline=calibration, train_rows=60, development_rows=24,
                  max_train_tokens=max(r["input_tokens"] for r in train), max_development_tokens=max(r["input_tokens"] for r in dev),
                  total_train_input_tokens=sum(r["input_tokens"] for r in train), total_train_target_tokens=sum(r["target_tokens"] for r in train),
                  longest_train_rows=sorted(((r["input_tokens"], r["id"]) for r in train), reverse=True)[:5],
                  train_jsonl_sha256=sha(OUT / "train.jsonl"), development_jsonl_sha256=sha(OUT / "development.jsonl"), messages_jsonl_sha256=sha(OUT / "messages.jsonl"),
                  no_truncation=True, decoded_target_matches_every_answer=True, prompt_and_empty_reasoning_markup_masked=True,
                  development_policy="12 A/B no-gradient loss views only; excluded from optimizer records",
                  shared_presentation_changes=["TR058 S010 validated fit overlay", "TR049 optional comma whitespace removed with exact AST equality",
                                               "DV008 development target combining accent escaped (exact AST equality)"],
                  script_sha256=sha(pathlib.Path(__file__)))
    (OUT / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (OUT / "authorization.json").write_text(json.dumps(dict(
        status="none", note="Staged packets only. The user approved the candidate-008 corpus hash (USER_REVIEW_2026-11-05.json) but has not "
        "authorized a training export or a training run. A consumer must find an explicit authorization naming messages_jsonl_sha256 "
        "and train_jsonl_sha256 from report.json before using these files.",
        messages_jsonl_sha256=report["messages_jsonl_sha256"], train_jsonl_sha256=report["train_jsonl_sha256"]), indent=2) + "\n", encoding="utf-8")
    print("REPORT_JSON:" + json.dumps(report, separators=(",", ":")))


if __name__ == "__main__":
    main()
