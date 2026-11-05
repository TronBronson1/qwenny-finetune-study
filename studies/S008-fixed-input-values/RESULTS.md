# S008 fixed-input value results

Completed November 4, 2026. Existing weights only. See [frozen protocol](PROTOCOL.md) and [interpretation](INTERPRETATION.md).

| Model | Split | Correct values / planned | Typed correct | All-four tasks | Parseable tasks |
|---|---|---:|---:|---:|---:|
| base | training | 13/16 | 13 | 3/4 | 4/4 |
| base | development | 9/16 | 9 | 0/4 | 4/4 |
| original-e1 | training | 14/16 | 14 | 3/4 | 4/4 |
| original-e1 | development | 9/16 | 9 | 0/4 | 4/4 |
| original-e5 | training | 12/16 | 12 | 3/4 | 3/4 |
| original-e5 | development | 10/16 | 10 | 0/4 | 4/4 |

| Task | Model | Correct/4 | Parse error |
|---|---|---:|---|
| TR024 | base | 4/4 | none |
| TR024 | original-e1 | 4/4 | none |
| TR024 | original-e5 | 4/4 | none |
| DV008 | original-e1 | 3/4 | none |
| DV008 | original-e5 | 3/4 | none |
| DV008 | base | 3/4 | none |
| TR025 | original-e5 | 0/4 | Expecting value: line 1 column 7 (char 6) |
| TR025 | base | 4/4 | none |
| TR025 | original-e1 | 4/4 | none |
| DV004 | base | 3/4 | none |
| DV004 | original-e1 | 3/4 | none |
| DV004 | original-e5 | 3/4 | none |
| TR038 | original-e1 | 4/4 | none |
| TR038 | original-e5 | 4/4 | none |
| TR038 | base | 4/4 | none |
| DV011 | original-e5 | 2/4 | none |
| DV011 | base | 2/4 | none |
| DV011 | original-e1 | 2/4 | none |
| TR049 | base | 1/4 | none |
| TR049 | original-e1 | 2/4 | none |
| TR049 | original-e5 | 4/4 | none |
| DV007 | original-e1 | 1/4 | none |
| DV007 | original-e5 | 2/4 | none |
| DV007 | base | 1/4 | none |

All 24 responses terminated. Total process time: 179.4s; generation: 90.5s; output tokens: 654. No cap hit, repair, retry, code execution, optimizer update, cloud, app closure or final/regression access.

Primary score includes parse failures as zero, preserving the planned denominator. Exact Python tuple identity/type is outside this JSON-normalized component metric. One greedy condition on eight purposive visible tasks cannot establish general aptitude or practical adapter adoption.

[Machine results](results.json) · [Raw generation report](../../training-v1/probes/s008-001/report.json) · [Expected inputs/outputs](selection.json)
