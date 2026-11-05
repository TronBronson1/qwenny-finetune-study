# Generated tables (make_report.py)

Generated 2026-11-05T02:28:54Z from commit `657fe3de188d`; Python 3.13.18, pytest 9.2.0. Do not edit by hand.

## Totals

| Metric | Value |
|---|---:|
| tasks | 72 |
| generated | 1134 |
| applicable | 973 |
| gap 007 | 76 |
| gap 008 | 19 |
| fixed | 57 |
| still open | 19 |
| new in 008 | 0 |
| tasks with gap 007 | 42 |
| tasks with gap 008 | 17 |

## By requirement family

| Family | Generated | Differs (applicable) | No difference found | Gaps 007 | Gaps 008 | Fixed | Still open | New in 008 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| type-subclass | 129 | 129 | 0 | 0 | 0 | 0 | 0 | 0 |
| type-ordinary | 129 | 120 | 9 | 28 | 0 | 28 | 0 | 0 |
| type-bool | 67 | 67 | 0 | 0 | 0 | 0 | 0 | 0 |
| return-subclass | 103 | 97 | 6 | 0 | 0 | 0 | 0 | 0 |
| return-swap | 103 | 35 | 68 | 0 | 0 | 0 | 0 | 0 |
| order | 72 | 22 | 50 | 4 | 0 | 4 | 0 | 0 |
| exception-class | 124 | 124 | 0 | 0 | 0 | 0 | 0 | 0 |
| mutation-valid | 40 | 37 | 3 | 4 | 0 | 4 | 0 | 0 |
| ascii | 49 | 46 | 3 | 12 | 0 | 12 | 0 | 0 |
| boundary | 271 | 257 | 14 | 9 | 0 | 9 | 0 | 0 |
| case | 28 | 20 | 8 | 0 | 0 | 0 | 0 | 0 |
| mutation-error | 19 | 19 | 0 | 19 | 19 | 0 | 19 | 0 |

## Previously reported gaps

| Task | Gap | Mutants | candidate-007 | candidate-008 |
|---|---|---|---|---|
| TR038 | non-ASCII hex digits accepted | A-unicode-decimal-digits, A-nfkc-normalize | covered | covered |
| TR043 | non-ASCII binary digits accepted | A-unicode-decimal-digits, A-nfkc-normalize | covered | covered |
| TR044 | non-ASCII decimal endpoints accepted | A-unicode-decimal-digits, A-nfkc-normalize, A-predicate-4 | gap | covered |
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

| Task | Split | Applicable | Gaps 007 | Gaps 008 | Fixed | Still open (008) | New in 008 |
|---|---|---:|---:|---:|---:|---|---|
| DV001 | dev | 12 | 0 | 0 | 0 | - | - |
| DV002 | dev | 17 | 0 | 0 | 0 | - | - |
| DV003 | dev | 14 | 0 | 0 | 0 | - | - |
| DV004 | dev | 17 | 2 | 1 | 1 | M-values-on-error | - |
| DV005 | dev | 7 | 1 | 0 | 1 | - | - |
| DV006 | dev | 11 | 1 | 0 | 1 | - | - |
| DV007 | dev | 50 | 1 | 0 | 1 | - | - |
| DV008 | dev | 10 | 0 | 0 | 0 | - | - |
| DV009 | dev | 24 | 1 | 1 | 0 | M-values-on-error | - |
| DV010 | dev | 23 | 6 | 1 | 5 | M-tokens-on-error | - |
| DV011 | dev | 33 | 8 | 1 | 7 | M-intervals-on-error | - |
| DV012 | dev | 5 | 1 | 0 | 1 | - | - |
| TR001 | tra | 14 | 0 | 0 | 0 | - | - |
| TR002 | tra | 10 | 0 | 0 | 0 | - | - |
| TR003 | tra | 8 | 0 | 0 | 0 | - | - |
| TR004 | tra | 14 | 0 | 0 | 0 | - | - |
| TR005 | tra | 5 | 0 | 0 | 0 | - | - |
| TR006 | tra | 14 | 1 | 0 | 1 | - | - |
| TR007 | tra | 8 | 0 | 0 | 0 | - | - |
| TR008 | tra | 8 | 1 | 0 | 1 | - | - |
| TR009 | tra | 8 | 0 | 0 | 0 | - | - |
| TR010 | tra | 8 | 1 | 0 | 1 | - | - |
| TR011 | tra | 12 | 0 | 0 | 0 | - | - |
| TR012 | tra | 15 | 0 | 0 | 0 | - | - |
| TR013 | tra | 19 | 1 | 0 | 1 | - | - |
| TR014 | tra | 7 | 3 | 0 | 3 | - | - |
| TR015 | tra | 7 | 2 | 0 | 2 | - | - |
| TR016 | tra | 5 | 2 | 0 | 2 | - | - |
| TR017 | tra | 8 | 2 | 0 | 2 | - | - |
| TR018 | tra | 7 | 0 | 0 | 0 | - | - |
| TR019 | tra | 4 | 0 | 0 | 0 | - | - |
| TR020 | tra | 4 | 1 | 0 | 1 | - | - |
| TR021 | tra | 11 | 0 | 0 | 0 | - | - |
| TR022 | tra | 4 | 1 | 0 | 1 | - | - |
| TR023 | tra | 11 | 1 | 0 | 1 | - | - |
| TR024 | tra | 13 | 3 | 0 | 3 | - | - |
| TR025 | tra | 13 | 1 | 1 | 0 | M-values-on-error | - |
| TR026 | tra | 12 | 1 | 1 | 0 | M-values-on-error | - |
| TR027 | tra | 16 | 1 | 1 | 0 | M-values-on-error | - |
| TR028 | tra | 12 | 1 | 1 | 0 | M-values-on-error | - |
| TR029 | tra | 21 | 3 | 1 | 2 | M-values-on-error | - |
| TR030 | tra | 20 | 5 | 1 | 4 | M-matrix-on-error | - |
| TR031 | tra | 22 | 2 | 2 | 0 | M-left-on-error, M-right-on-error | - |
| TR032 | tra | 19 | 1 | 1 | 0 | M-values-on-error | - |
| TR033 | tra | 20 | 2 | 1 | 1 | M-values-on-error | - |
| TR034 | tra | 26 | 2 | 1 | 1 | M-values-on-error | - |
| TR035 | tra | 16 | 1 | 1 | 0 | M-values-on-error | - |
| TR036 | tra | 15 | 1 | 1 | 0 | M-values-on-error | - |
| TR037 | tra | 10 | 1 | 0 | 1 | - | - |
| TR038 | tra | 8 | 0 | 0 | 0 | - | - |
| TR039 | tra | 7 | 0 | 0 | 0 | - | - |
| TR040 | tra | 7 | 0 | 0 | 0 | - | - |
| TR041 | tra | 12 | 1 | 0 | 1 | - | - |
| TR042 | tra | 12 | 1 | 0 | 1 | - | - |
| TR043 | tra | 9 | 0 | 0 | 0 | - | - |
| TR044 | tra | 10 | 1 | 0 | 1 | - | - |
| TR045 | tra | 6 | 0 | 0 | 0 | - | - |
| TR046 | tra | 10 | 0 | 0 | 0 | - | - |
| TR047 | tra | 17 | 0 | 0 | 0 | - | - |
| TR048 | tra | 12 | 1 | 0 | 1 | - | - |
| TR049 | tra | 28 | 0 | 0 | 0 | - | - |
| TR050 | tra | 24 | 1 | 0 | 1 | - | - |
| TR051 | tra | 12 | 0 | 0 | 0 | - | - |
| TR052 | tra | 10 | 0 | 0 | 0 | - | - |
| TR053 | tra | 7 | 0 | 0 | 0 | - | - |
| TR054 | tra | 7 | 0 | 0 | 0 | - | - |
| TR055 | tra | 19 | 0 | 0 | 0 | - | - |
| TR056 | tra | 10 | 0 | 0 | 0 | - | - |
| TR057 | tra | 9 | 1 | 0 | 1 | - | - |
| TR058 | tra | 18 | 2 | 0 | 2 | - | - |
| TR059 | tra | 29 | 4 | 2 | 2 | M-left-on-error, M-right-on-error | - |
| TR060 | tra | 21 | 2 | 0 | 2 | - | - |

## Gaps still open in candidate-008 (19)

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

## Gaps new in candidate-008 (0)

| Task | Mutant | Requirement | Witness args | Reference | Mutant |
|---|---|---|---|---|---|

## Gaps fixed by candidate-008 (57)

| Task | Mutant | Requirement | Witness args | Reference | Mutant |
|---|---|---|---|---|---|
| DV004 | `O-value-before-type` | type-before-value validation order | `([-1, 'x'],)` | raise 'TypeError' | raise 'ValueError' |
| DV005 | `T-text-L0-ordinary` | text level 0 (str): exact types: ordinary wrong type rejected | `(['('],)` | raise 'TypeError' | raise 'ValueError' |
| DV006 | `T-text-L0-ordinary` | text level 0 (str): exact types: ordinary wrong type rejected | `(['A'],)` | raise 'TypeError' | return ('str', "'2'") |
| DV007 | `B-op4:46:<-><=` | boundary off-by-one: op4:46:<-><= | `(0, 1, 1, 1)` | raise 'IndexError' | return ('list', (('tuple', (('int', '0'), ('int', '0'))),)) |
| DV010 | `T-tokens-L1-ordinary` | tokens level 1 (str): exact types: ordinary wrong type rejected | `(['+', 1],)` | raise 'TypeError' | raise 'ValueError' |
| DV010 | `O-value-before-type` | type-before-value validation order | `([1, 1],)` | raise 'TypeError' | raise 'ValueError' |
| DV010 | `B-num7:26:2->1` | boundary off-by-one: num7:26:2->1 | `(['4', '+'],)` | raise 'ValueError' | raise 'IndexError' |
| DV010 | `B-re10:{0,3}:2:3->2` | boundary off-by-one: re10:{0,3}:2:3->2 | `(['9999'],)` | return ('int', '9999') | raise 'ValueError' |
| DV010 | `B-re10:{0,3}:2:3->4` | boundary off-by-one: re10:{0,3}:2:3->4 | `(['10000'],)` | raise 'ValueError' | return ('int', '10000') |
| DV011 | `T-intervals-L0-ordinary` | intervals level 0 (list): exact types: ordinary wrong type rejected | `((),)` | raise 'TypeError' | return ('list', ()) |
| DV011 | `T-intervals-L1-ordinary` | intervals level 1 (tuple): exact types: ordinary wrong type rejected | `([[1, 2]],)` | raise 'TypeError' | return ('list', (('tuple', (('int', '1'), ('int', '2'))),)) |
| DV011 | `O-value-before-type` | type-before-value validation order | `([(1,), -1],)` | raise 'TypeError' | raise 'ValueError' |
| DV011 | `B-num6:35:1->0` | boundary off-by-one: num6:35:1->0 | `([(2, 60), (-3, -1), (10, 100)],)` | return ('list', (('tuple', (('int', '-3'), ('int', '-1'))), ('tuple', (('int', '2'), ('int | return ('list', (('tuple', (('int', '-3'), ('int', '-1'))), ('tuple', (('int', '2'), ('int |
| DV011 | `B-num6:50:1->0` | boundary off-by-one: num6:50:1->0 | `([(2, 60), (-3, -1), (10, 100)],)` | return ('list', (('tuple', (('int', '-3'), ('int', '-1'))), ('tuple', (('int', '2'), ('int | return ('list', (('tuple', (('int', '2'), ('int', '100'))), ('tuple', (('int', '2'), ('int |
| DV011 | `B-num6:62:1->0` | boundary off-by-one: num6:62:1->0 | `([(2, 60), (-3, -1), (10, 100)],)` | return ('list', (('tuple', (('int', '-3'), ('int', '-1'))), ('tuple', (('int', '2'), ('int | return ('list', (('tuple', (('int', '-3'), ('int', '-1'))), ('tuple', (('int', '-3'), ('in |
| DV011 | `B-num6:85:1->0` | boundary off-by-one: num6:85:1->0 | `([(1, 2), (26, 27), (25, 130), (25, 256)],)` | return ('list', (('tuple', (('int', '1'), ('int', '2'))), ('tuple', (('int', '25'), ('int' | return ('list', (('tuple', (('int', '1'), ('int', '2'))), ('tuple', (('int', '25'), ('int' |
| DV012 | `T-text-L0-ordinary` | text level 0 (str): exact types: ordinary wrong type rejected | `(['('],)` | raise 'TypeError' | return ('bool', 'False') |
| TR006 | `T-number-L0-ordinary` | number level 0 (int): exact types: ordinary wrong type rejected | `(-1.5,)` | raise 'TypeError' | raise 'ValueError' |
| TR008 | `T-number-L0-ordinary` | number level 0 (int): exact types: ordinary wrong type rejected | `(-1.5,)` | raise 'TypeError' | raise 'ValueError' |
| TR010 | `T-number-L0-ordinary` | number level 0 (int): exact types: ordinary wrong type rejected | `(-1.5,)` | raise 'TypeError' | raise 'ValueError' |
| TR013 | `T-number-L0-ordinary` | number level 0 (int): exact types: ordinary wrong type rejected | `(-1.5, 2)` | raise 'TypeError' | raise 'ValueError' |
| TR014 | `T-text-L0-ordinary` | text level 0 (str): exact types: ordinary wrong type rejected | `(['a'],)` | raise 'TypeError' | return ('str', "'a'") |
| TR014 | `A-unicode-decimal-digits` | ASCII-only rule: unicode-decimal-digits | `('=４',)` | return ('str', "'=４'") | return ('str', "'=4'") |
| TR014 | `A-predicate-6` | ASCII-only rule: 'char != " "' -> 'not char.isspace()' | `('a \tb',)` | return ('str', "'a \\tb'") | return ('str', "'a b'") |
| TR015 | `A-unicode-decimal-digits` | ASCII-only rule: unicode-decimal-digits | `('  ١',)` | return ('str', "'١'") | return ('str', "'1'") |
| TR015 | `A-nfkc-normalize` | ASCII-only rule: nfkc-normalize | `('  ｅ',)` | return ('str', "'ｅ'") | return ('str', "'e'") |
| TR016 | `T-text-L0-ordinary` | text level 0 (str): exact types: ordinary wrong type rejected | `(['a'],)` | raise 'TypeError' | return ('int', '1') |
| TR016 | `A-nfkc-normalize` | ASCII-only rule: nfkc-normalize | `('Ｅá',)` | return ('int', '0') | return ('int', '1') |
| TR017 | `T-left-L0-ordinary` | left level 0 (str): exact types: ordinary wrong type rejected | `(['a'], 'b')` | raise 'TypeError' | return ('str', "'ab'") |
| TR017 | `T-right-L0-ordinary` | right level 0 (str): exact types: ordinary wrong type rejected | `('a', ['b'])` | raise 'TypeError' | return ('str', "'ab'") |
| TR020 | `T-text-L0-ordinary` | text level 0 (str): exact types: ordinary wrong type rejected | `(['a'],)` | raise 'TypeError' | return ('str', "'a'") |
| TR022 | `T-text-L0-ordinary` | text level 0 (str): exact types: ordinary wrong type rejected | `(['a'],)` | raise 'TypeError' | return ('list', (('str', "'a'"),)) |
| TR023 | `T-noun-L0-ordinary` | noun level 0 (str): exact types: ordinary wrong type rejected | `(-1, 1)` | raise 'TypeError' | raise 'ValueError' |
| TR024 | `T-text-L0-ordinary` | text level 0 (str): exact types: ordinary wrong type rejected | `(['a'],)` | raise 'TypeError' | return ('str', "'A'") |
| TR024 | `A-unicode-decimal-digits` | ASCII-only rule: unicode-decimal-digits | `('ǅ١ｅ',)` | return ('str', "'ǅ١ｅ'") | return ('str', "'ǅ1ｅ'") |
| TR024 | `A-nfkc-normalize` | ASCII-only rule: nfkc-normalize | `('ǅ١ｅ',)` | return ('str', "'ǅ١ｅ'") | return ('str', "'Dž١E'") |
| TR029 | `T-width-L0-ordinary` | width level 0 (int): exact types: ordinary wrong type rejected | `([], -1.5)` | raise 'TypeError' | raise 'ValueError' |
| TR029 | `M-values-sort` | values: no input mutation (valid calls) (sort) | `([4, 2], 2)` | return ('list', (('list', (('int', '4'), ('int', '2'))),)) | return ('list', (('list', (('int', '4'), ('int', '2'))),)); args after: ('tuple', (('list', (('int', '2'), ('int', '4'))), ('int', '2'))) |
| TR030 | `T-matrix-L0-ordinary` | matrix level 0 (list): exact types: ordinary wrong type rejected | `((),)` | raise 'TypeError' | return ('list', ()) |
| TR030 | `T-matrix-L1-ordinary` | matrix level 1 (list): exact types: ordinary wrong type rejected | `([(1,)],)` | raise 'TypeError' | return ('list', (('list', (('int', '1'),)),)) |
| TR030 | `O-value-before-type` | type-before-value validation order | `([[1], None, [1, 2]],)` | raise 'TypeError' | raise 'ValueError' |
| TR030 | `M-matrix-sort` | matrix: no input mutation (valid calls) (sort) | `([[59], [1]],)` | return ('list', (('list', (('int', '59'), ('int', '1'))),)) | return ('list', (('list', (('int', '59'), ('int', '1'))),)); args after: ('tuple', (('list', (('list', (('int', '1'),)), ('list', (('int',  |
| TR033 | `M-values-sort` | values: no input mutation (valid calls) (sort) | `([4, 2], 0)` | return ('list', (('int', '2'),)) | return ('list', (('int', '2'),)); args after: ('tuple', (('list', (('int', '2'), ('int', '4'))), ('int', '0'))) |
| TR034 | `M-values-sort` | values: no input mutation (valid calls) (sort) | `([3, 1, 2], 0, 3)` | return ('list', (('int', '3'), ('int', '1'), ('int', '2'))) | return ('list', (('int', '3'), ('int', '1'), ('int', '2'))); args after: ('tuple', (('list', (('int', '1'), ('int', '2'), ('int', '3'))), ( |
| TR037 | `A-predicate-4` | ASCII-only rule: '[0-9]' -> '\d' | `('1٠',)` | raise 'ValueError' | return ('int', '10') |
| TR041 | `A-predicate-4` | ASCII-only rule: '[0-9]' -> '\d' | `('1٠,2',)` | raise 'ValueError' | return ('tuple', (('int', '10'), ('int', '2'))) |
| TR042 | `A-predicate-4` | ASCII-only rule: '[0-9]' -> '\d' | `('1٠.0.0',)` | raise 'ValueError' | return ('tuple', (('int', '10'), ('int', '0'), ('int', '0'))) |
| TR044 | `A-predicate-4` | ASCII-only rule: '[0-9]' -> '\d' | `('[0:1٠]',)` | raise 'ValueError' | return ('tuple', (('int', '0'), ('int', '10'))) |
| TR048 | `T-number-L0-ordinary` | number level 0 (int): exact types: ordinary wrong type rejected | `(-1.5,)` | raise 'TypeError' | raise 'ValueError' |
| TR050 | `B-op3:28:<=-><` | boundary off-by-one: op3:28:<=->< | `(0, 1, 0)` | raise 'ValueError' | raise 'IndexError' |
| TR057 | `T-text-L0-ordinary` | text level 0 (str): exact types: ordinary wrong type rejected | `(['a'],)` | raise 'TypeError' | raise 'AttributeError' |
| TR058 | `T-left-L0-ordinary` | left level 0 (tuple): exact types: ordinary wrong type rejected | `([0, 0, 0], (0, 0, 0, 0))` | raise 'TypeError' | raise 'ValueError' |
| TR058 | `T-right-L0-ordinary` | right level 0 (tuple): exact types: ordinary wrong type rejected | `((0, 0), [0, 0, 0])` | raise 'TypeError' | raise 'ValueError' |
| TR059 | `T-left-L0-ordinary` | left level 0 (list): exact types: ordinary wrong type rejected | `((2, 1), [])` | raise 'TypeError' | raise 'ValueError' |
| TR059 | `T-right-L0-ordinary` | right level 0 (list): exact types: ordinary wrong type rejected | `([], (2, 1))` | raise 'TypeError' | raise 'ValueError' |
| TR060 | `T-text-L0-ordinary` | text level 0 (str): exact types: ordinary wrong type rejected | `(['a'],)` | raise 'TypeError' | return ('tuple', (('int', '1'), ('int', '0'), ('int', '0'))) |
| TR060 | `A-nfkc-normalize` | ASCII-only rule: nfkc-normalize | `('ǅＡ١',)` | return ('tuple', (('int', '0'), ('int', '0'), ('int', '3'))) | return ('tuple', (('int', '2'), ('int', '0'), ('int', '2'))) |

## Anomalies

- DV009 B-op5:13:<-><= candidate-007: pytest timeout (120.1 s; mutant loops forever) - counted as killed
- DV009 B-op5:13:<-><= candidate-008: pytest timeout (120.1 s; mutant loops forever) - counted as killed
- DV009 B-num7:45:1->0 candidate-007: pytest timeout (120.1 s; mutant loops forever) - counted as killed
- DV009 B-num7:45:1->0 candidate-008: pytest timeout (120.1 s; mutant loops forever) - counted as killed
- TR013 B-num3:25:2->1 candidate-007: pytest timeout (120.1 s; mutant loops forever) - counted as killed
- TR013 B-num3:25:2->1 candidate-008: pytest timeout (120.1 s; mutant loops forever) - counted as killed
- TR021 B-num4:84:1->0 candidate-007: pytest timeout (120.1 s; mutant loops forever) - counted as killed
- TR021 B-num4:84:1->0 candidate-008: pytest timeout (120.1 s; mutant loops forever) - counted as killed
- TR059 B-num6:59:1->0 candidate-007: pytest timeout (120.5 s; mutant loops forever) - counted as killed
- TR059 B-num6:59:1->0 candidate-008: pytest timeout (120.41 s; mutant loops forever) - counted as killed
