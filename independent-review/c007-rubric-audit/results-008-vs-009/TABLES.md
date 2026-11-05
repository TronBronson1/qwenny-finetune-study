# Generated tables (make_report.py)

Generated 2026-11-05T03:15:25Z from commit `b4997db125c4`; Python 3.13.18, pytest 9.2.0. Do not edit by hand.

## Totals

| Metric | Value |
|---|---:|
| tasks | 72 |
| generated | 1134 |
| applicable | 973 |
| gap 008 | 19 |
| gap 009 | 0 |
| fixed | 19 |
| still open | 0 |
| new in 009 | 0 |
| tasks with gap 008 | 17 |
| tasks with gap 009 | 0 |

## By requirement family

| Family | Generated | Differs (applicable) | No difference found | Gaps 008 | Gaps 009 | Fixed | Still open | New in 009 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| type-subclass | 129 | 129 | 0 | 0 | 0 | 0 | 0 | 0 |
| type-ordinary | 129 | 120 | 9 | 0 | 0 | 0 | 0 | 0 |
| type-bool | 67 | 67 | 0 | 0 | 0 | 0 | 0 | 0 |
| return-subclass | 103 | 97 | 6 | 0 | 0 | 0 | 0 | 0 |
| return-swap | 103 | 35 | 68 | 0 | 0 | 0 | 0 | 0 |
| order | 72 | 22 | 50 | 0 | 0 | 0 | 0 | 0 |
| exception-class | 124 | 124 | 0 | 0 | 0 | 0 | 0 | 0 |
| mutation-valid | 40 | 37 | 3 | 0 | 0 | 0 | 0 | 0 |
| ascii | 49 | 46 | 3 | 0 | 0 | 0 | 0 | 0 |
| boundary | 271 | 257 | 14 | 0 | 0 | 0 | 0 | 0 |
| case | 28 | 20 | 8 | 0 | 0 | 0 | 0 | 0 |
| mutation-error | 19 | 19 | 0 | 19 | 0 | 19 | 0 | 0 |

## Previously reported gaps

| Task | Gap | Mutants | candidate-008 | candidate-009 |
|---|---|---|---|---|
| TR038 | non-ASCII hex digits accepted | A-unicode-decimal-digits, A-nfkc-normalize | covered | covered |
| TR043 | non-ASCII binary digits accepted | A-unicode-decimal-digits, A-nfkc-normalize | covered | covered |
| TR044 | non-ASCII decimal endpoints accepted | A-unicode-decimal-digits, A-nfkc-normalize, A-predicate-4 | covered | covered |
| TR056 | non-ASCII RGB hex digits accepted | A-unicode-decimal-digits, A-nfkc-normalize | covered | covered |
| DV010 | non-ASCII RPN digits accepted | A-unicode-decimal-digits, A-nfkc-normalize | covered | covered |
| DV008 | case-insensitive comparison | C-input-fold-lower, C-input-fold-upper | covered | covered |
| DV011 | int-subclass endpoints accepted | T-intervals-L2-subclass | covered | covered |
| TR026 | plain wrong-type list element accepted | T-values-L1-ordinary | covered | covered |
| TR027 | plain wrong-type list element accepted | T-values-L1-ordinary | covered | covered |
| TR028 | plain wrong-type list element accepted | T-values-L1-ordinary | covered | covered |
| TR029 | plain wrong-type list element accepted | T-values-L1-ordinary | covered | covered |
| TR030 | plain wrong-type list element accepted | T-matrix-L2-ordinary | covered | covered |
| TR031 | plain wrong-type list element accepted | T-left-L1-ordinary, T-right-L1-ordinary | covered | covered |
| TR032 | plain wrong-type list element accepted | T-values-L1-ordinary | covered | covered |
| TR033 | plain wrong-type list element accepted | T-values-L1-ordinary | covered | covered |
| TR034 | plain wrong-type list element accepted | T-values-L1-ordinary | covered | covered |
| TR035 | plain wrong-type list element accepted | T-values-L1-ordinary | covered | covered |
| TR036 | plain wrong-type list element accepted | T-values-L1-ordinary | covered | covered |
| TR058 | plain wrong-type list element accepted | T-left-L1-ordinary, T-right-L1-ordinary | covered | covered |
| TR059 | plain wrong-type list element accepted | T-left-L1-ordinary, T-right-L1-ordinary | covered | covered |
| DV004 | plain wrong-type list element accepted | T-values-L1-ordinary | covered | covered |
| DV009 | plain wrong-type list element accepted | T-values-L1-ordinary | covered | covered |
| DV011 | plain wrong-type list element accepted | T-intervals-L2-ordinary | covered | covered |

## Per task

| Task | Split | Applicable | Gaps 008 | Gaps 009 | Fixed | Still open (009) | New in 009 |
|---|---|---:|---:|---:|---:|---|---|
| DV001 | dev | 12 | 0 | 0 | 0 | - | - |
| DV002 | dev | 17 | 0 | 0 | 0 | - | - |
| DV003 | dev | 14 | 0 | 0 | 0 | - | - |
| DV004 | dev | 17 | 1 | 0 | 1 | - | - |
| DV005 | dev | 7 | 0 | 0 | 0 | - | - |
| DV006 | dev | 11 | 0 | 0 | 0 | - | - |
| DV007 | dev | 50 | 0 | 0 | 0 | - | - |
| DV008 | dev | 10 | 0 | 0 | 0 | - | - |
| DV009 | dev | 24 | 1 | 0 | 1 | - | - |
| DV010 | dev | 23 | 1 | 0 | 1 | - | - |
| DV011 | dev | 33 | 1 | 0 | 1 | - | - |
| DV012 | dev | 5 | 0 | 0 | 0 | - | - |
| TR001 | tra | 14 | 0 | 0 | 0 | - | - |
| TR002 | tra | 10 | 0 | 0 | 0 | - | - |
| TR003 | tra | 8 | 0 | 0 | 0 | - | - |
| TR004 | tra | 14 | 0 | 0 | 0 | - | - |
| TR005 | tra | 5 | 0 | 0 | 0 | - | - |
| TR006 | tra | 14 | 0 | 0 | 0 | - | - |
| TR007 | tra | 8 | 0 | 0 | 0 | - | - |
| TR008 | tra | 8 | 0 | 0 | 0 | - | - |
| TR009 | tra | 8 | 0 | 0 | 0 | - | - |
| TR010 | tra | 8 | 0 | 0 | 0 | - | - |
| TR011 | tra | 12 | 0 | 0 | 0 | - | - |
| TR012 | tra | 15 | 0 | 0 | 0 | - | - |
| TR013 | tra | 19 | 0 | 0 | 0 | - | - |
| TR014 | tra | 7 | 0 | 0 | 0 | - | - |
| TR015 | tra | 7 | 0 | 0 | 0 | - | - |
| TR016 | tra | 5 | 0 | 0 | 0 | - | - |
| TR017 | tra | 8 | 0 | 0 | 0 | - | - |
| TR018 | tra | 7 | 0 | 0 | 0 | - | - |
| TR019 | tra | 4 | 0 | 0 | 0 | - | - |
| TR020 | tra | 4 | 0 | 0 | 0 | - | - |
| TR021 | tra | 11 | 0 | 0 | 0 | - | - |
| TR022 | tra | 4 | 0 | 0 | 0 | - | - |
| TR023 | tra | 11 | 0 | 0 | 0 | - | - |
| TR024 | tra | 13 | 0 | 0 | 0 | - | - |
| TR025 | tra | 13 | 1 | 0 | 1 | - | - |
| TR026 | tra | 12 | 1 | 0 | 1 | - | - |
| TR027 | tra | 16 | 1 | 0 | 1 | - | - |
| TR028 | tra | 12 | 1 | 0 | 1 | - | - |
| TR029 | tra | 21 | 1 | 0 | 1 | - | - |
| TR030 | tra | 20 | 1 | 0 | 1 | - | - |
| TR031 | tra | 22 | 2 | 0 | 2 | - | - |
| TR032 | tra | 19 | 1 | 0 | 1 | - | - |
| TR033 | tra | 20 | 1 | 0 | 1 | - | - |
| TR034 | tra | 26 | 1 | 0 | 1 | - | - |
| TR035 | tra | 16 | 1 | 0 | 1 | - | - |
| TR036 | tra | 15 | 1 | 0 | 1 | - | - |
| TR037 | tra | 10 | 0 | 0 | 0 | - | - |
| TR038 | tra | 8 | 0 | 0 | 0 | - | - |
| TR039 | tra | 7 | 0 | 0 | 0 | - | - |
| TR040 | tra | 7 | 0 | 0 | 0 | - | - |
| TR041 | tra | 12 | 0 | 0 | 0 | - | - |
| TR042 | tra | 12 | 0 | 0 | 0 | - | - |
| TR043 | tra | 9 | 0 | 0 | 0 | - | - |
| TR044 | tra | 10 | 0 | 0 | 0 | - | - |
| TR045 | tra | 6 | 0 | 0 | 0 | - | - |
| TR046 | tra | 10 | 0 | 0 | 0 | - | - |
| TR047 | tra | 17 | 0 | 0 | 0 | - | - |
| TR048 | tra | 12 | 0 | 0 | 0 | - | - |
| TR049 | tra | 28 | 0 | 0 | 0 | - | - |
| TR050 | tra | 24 | 0 | 0 | 0 | - | - |
| TR051 | tra | 12 | 0 | 0 | 0 | - | - |
| TR052 | tra | 10 | 0 | 0 | 0 | - | - |
| TR053 | tra | 7 | 0 | 0 | 0 | - | - |
| TR054 | tra | 7 | 0 | 0 | 0 | - | - |
| TR055 | tra | 19 | 0 | 0 | 0 | - | - |
| TR056 | tra | 10 | 0 | 0 | 0 | - | - |
| TR057 | tra | 9 | 0 | 0 | 0 | - | - |
| TR058 | tra | 18 | 0 | 0 | 0 | - | - |
| TR059 | tra | 29 | 2 | 0 | 2 | - | - |
| TR060 | tra | 21 | 0 | 0 | 0 | - | - |

## Gaps still open in candidate-009 (0)

| Task | Mutant | Requirement | Witness args | Reference | Mutant |
|---|---|---|---|---|---|

## Gaps new in candidate-009 (0)

| Task | Mutant | Requirement | Witness args | Reference | Mutant |
|---|---|---|---|---|---|

## Gaps fixed by candidate-009 (19)

| Task | Mutant | Requirement | Witness args | Reference | Mutant |
|---|---|---|---|---|---|
| DV004 | `M-values-on-error` | values: no input mutation (error path; contract-only) | `([-1],)` | raise 'ValueError' | raise 'ValueError'; args after: ('tuple', (('list', (('int', '-1'), ('int', '-1'))),)) |
| DV009 | `M-values-on-error` | values: no input mutation (error path; contract-only) | `([], 1.5)` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('list', (('int', '0'),)), ('float', '1.5'))) |
| DV010 | `M-tokens-on-error` | tokens: no input mutation (error path; contract-only) | `([],)` | raise 'ValueError' | raise 'ValueError'; args after: ('tuple', (('list', (('str', "''"),)),)) |
| DV011 | `M-intervals-on-error` | intervals: no input mutation (error path; contract-only) | `([1],)` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('list', (('int', '1'), ('int', '1'))),)) |
| TR025 | `M-values-on-error` | values: no input mutation (error path; contract-only) | `([1],)` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('list', (('int', '1'), ('int', '1'))),)) |
| TR026 | `M-values-on-error` | values: no input mutation (error path; contract-only) | `(['x'],)` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('list', (('str', "'x'"), ('str', "'x'"))),)) |
| TR027 | `M-values-on-error` | values: no input mutation (error path; contract-only) | `(['x'],)` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('list', (('str', "'x'"), ('str', "'x'"))),)) |
| TR028 | `M-values-on-error` | values: no input mutation (error path; contract-only) | `(['x'],)` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('list', (('str', "'x'"), ('str', "'x'"))),)) |
| TR029 | `M-values-on-error` | values: no input mutation (error path; contract-only) | `([], 0)` | raise 'ValueError' | raise 'ValueError'; args after: ('tuple', (('list', (('int', '0'),)), ('int', '0'))) |
| TR030 | `M-matrix-on-error` | matrix: no input mutation (error path; contract-only) | `([1],)` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('list', (('int', '1'), ('int', '1'))),)) |
| TR031 | `M-left-on-error` | left: no input mutation (error path; contract-only) | `([], 3)` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('list', (('int', '0'),)), ('int', '3'))) |
| TR031 | `M-right-on-error` | right: no input mutation (error path; contract-only) | `(3, [])` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('int', '3'), ('list', (('int', '0'),)))) |
| TR032 | `M-values-on-error` | values: no input mutation (error path; contract-only) | `(['x'],)` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('list', (('str', "'x'"), ('str', "'x'"))),)) |
| TR033 | `M-values-on-error` | values: no input mutation (error path; contract-only) | `([], 0)` | raise 'IndexError' | raise 'IndexError'; args after: ('tuple', (('list', (('int', '0'),)), ('int', '0'))) |
| TR034 | `M-values-on-error` | values: no input mutation (error path; contract-only) | `([], 1, 0)` | raise 'IndexError' | raise 'IndexError'; args after: ('tuple', (('list', (('int', '0'),)), ('int', '1'), ('int', '0'))) |
| TR035 | `M-values-on-error` | values: no input mutation (error path; contract-only) | `(['x'],)` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('list', (('str', "'x'"), ('str', "'x'"))),)) |
| TR036 | `M-values-on-error` | values: no input mutation (error path; contract-only) | `([],)` | raise 'ValueError' | raise 'ValueError'; args after: ('tuple', (('list', (('int', '0'),)),)) |
| TR059 | `M-left-on-error` | left: no input mutation (error path; contract-only) | `([], 3)` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('list', (('int', '0'),)), ('int', '3'))) |
| TR059 | `M-right-on-error` | right: no input mutation (error path; contract-only) | `(3, [])` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('int', '3'), ('list', (('int', '0'),)))) |

## Anomalies

- DV009 B-op5:13:<-><= candidate-008: pytest timeout (120.1 s; mutant loops forever) - counted as killed
- DV009 B-op5:13:<-><= candidate-009: pytest timeout (120.1 s; mutant loops forever) - counted as killed
- DV009 B-num7:45:1->0 candidate-008: pytest timeout (120.1 s; mutant loops forever) - counted as killed
- DV009 B-num7:45:1->0 candidate-009: pytest timeout (120.11 s; mutant loops forever) - counted as killed
- TR013 B-num3:25:2->1 candidate-008: pytest timeout (120.1 s; mutant loops forever) - counted as killed
- TR013 B-num3:25:2->1 candidate-009: pytest timeout (120.1 s; mutant loops forever) - counted as killed
- TR021 B-num4:84:1->0 candidate-008: pytest timeout (120.1 s; mutant loops forever) - counted as killed
- TR021 B-num4:84:1->0 candidate-009: pytest timeout (120.1 s; mutant loops forever) - counted as killed
- TR059 B-num6:59:1->0 candidate-008: pytest timeout (120.41 s; mutant loops forever) - counted as killed
- TR059 B-num6:59:1->0 candidate-009: pytest timeout (120.31 s; mutant loops forever) - counted as killed
