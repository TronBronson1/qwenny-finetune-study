# Generated tables (make_report.py)

Generated 2026-11-05T02:00:51Z from commit `b0e0227ed1b3`; Python 3.13.18, pytest 9.2.0. Do not edit by hand.

## Totals

| Metric | Value |
|---|---:|
| tasks | 72 |
| generated | 1134 |
| applicable | 973 |
| gap 006 | 121 |
| gap 007 | 76 |
| fixed | 45 |
| still open | 76 |
| new in 007 | 0 |
| tasks with gap 006 | 49 |
| tasks with gap 007 | 42 |

## By requirement family

| Family | Generated | Differs (applicable) | No difference found | Gaps 006 | Gaps 007 | Fixed | Still open | New in 007 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| type-subclass | 129 | 129 | 0 | 1 | 0 | 1 | 0 | 0 |
| type-ordinary | 129 | 120 | 9 | 47 | 28 | 19 | 28 | 0 |
| type-bool | 67 | 67 | 0 | 0 | 0 | 0 | 0 | 0 |
| return-subclass | 103 | 97 | 6 | 0 | 0 | 0 | 0 | 0 |
| return-swap | 103 | 35 | 68 | 0 | 0 | 0 | 0 | 0 |
| order | 72 | 22 | 50 | 4 | 4 | 0 | 4 | 0 |
| exception-class | 124 | 124 | 0 | 0 | 0 | 0 | 0 | 0 |
| mutation-valid | 40 | 37 | 3 | 4 | 4 | 0 | 4 | 0 |
| ascii | 49 | 46 | 3 | 31 | 12 | 19 | 12 | 0 |
| boundary | 271 | 257 | 14 | 11 | 9 | 2 | 9 | 0 |
| case | 28 | 20 | 8 | 4 | 0 | 4 | 0 | 0 |
| mutation-error | 19 | 19 | 0 | 19 | 19 | 0 | 19 | 0 |

## Previously reported gaps

| Task | Gap | Mutants | candidate-006 | candidate-007 |
|---|---|---|---|---|
| TR038 | non-ASCII hex digits accepted | A-unicode-decimal-digits, A-nfkc-normalize | gap | covered |
| TR043 | non-ASCII binary digits accepted | A-unicode-decimal-digits, A-nfkc-normalize | gap | covered |
| TR044 | non-ASCII decimal endpoints accepted | A-unicode-decimal-digits, A-nfkc-normalize, A-predicate-4 | gap | gap |
| TR056 | non-ASCII RGB hex digits accepted | A-unicode-decimal-digits, A-nfkc-normalize | gap | covered |
| DV010 | non-ASCII RPN digits accepted | A-unicode-decimal-digits, A-nfkc-normalize | gap | covered |
| DV008 | case-insensitive comparison | C-input-fold-lower, C-input-fold-upper | gap | covered |
| DV011 | int-subclass endpoints accepted | T-intervals-L2-subclass | gap | covered |
| TR026 | plain wrong-type list element accepted | T-values-L1-ordinary | gap | covered |
| TR027 | plain wrong-type list element accepted | T-values-L1-ordinary | gap | covered |
| TR028 | plain wrong-type list element accepted | T-values-L1-ordinary | gap | covered |
| TR029 | plain wrong-type list element accepted | T-values-L1-ordinary | gap | covered |
| TR030 | plain wrong-type list element accepted | T-matrix-L2-ordinary | gap | covered |
| TR031 | plain wrong-type list element accepted | T-left-L1-ordinary, T-right-L1-ordinary | gap | covered |
| TR032 | plain wrong-type list element accepted | T-values-L1-ordinary | gap | covered |
| TR033 | plain wrong-type list element accepted | T-values-L1-ordinary | gap | covered |
| TR034 | plain wrong-type list element accepted | T-values-L1-ordinary | gap | covered |
| TR035 | plain wrong-type list element accepted | T-values-L1-ordinary | gap | covered |
| TR036 | plain wrong-type list element accepted | T-values-L1-ordinary | gap | covered |
| TR058 | plain wrong-type list element accepted | T-left-L1-ordinary, T-right-L1-ordinary | gap | covered |
| TR059 | plain wrong-type list element accepted | T-left-L1-ordinary, T-right-L1-ordinary | gap | covered |
| DV004 | plain wrong-type list element accepted | T-values-L1-ordinary | gap | covered |
| DV009 | plain wrong-type list element accepted | T-values-L1-ordinary | gap | covered |
| DV011 | plain wrong-type list element accepted | T-intervals-L2-ordinary | gap | covered |

## Per task

| Task | Split | Applicable | Gaps 006 | Gaps 007 | Fixed | Still open (007) | New in 007 |
|---|---|---:|---:|---:|---:|---|---|
| DV001 | dev | 12 | 0 | 0 | 0 | - | - |
| DV002 | dev | 17 | 1 | 0 | 1 | - | - |
| DV003 | dev | 14 | 0 | 0 | 0 | - | - |
| DV004 | dev | 17 | 3 | 2 | 1 | O-value-before-type, M-values-on-error | - |
| DV005 | dev | 7 | 1 | 1 | 0 | T-text-L0-ordinary | - |
| DV006 | dev | 11 | 2 | 1 | 1 | T-text-L0-ordinary | - |
| DV007 | dev | 50 | 2 | 1 | 1 | B-op4:46:<-><= | - |
| DV008 | dev | 10 | 2 | 0 | 2 | - | - |
| DV009 | dev | 24 | 2 | 1 | 1 | M-values-on-error | - |
| DV010 | dev | 23 | 8 | 6 | 2 | T-tokens-L1-ordinary, O-value-before-type, M-tokens-on-error, B-num7:26:2->1, B-re10:{0,3}:2:3->2, B-re10:{0,3}:2:3->4 | - |
| DV011 | dev | 33 | 10 | 8 | 2 | T-intervals-L0-ordinary, T-intervals-L1-ordinary, O-value-before-type, M-intervals-on-error, B-num6:35:1->0, B-num6:50:1->0, B-num6:62:1->0, B-num6:85:1->0 | - |
| DV012 | dev | 5 | 1 | 1 | 0 | T-text-L0-ordinary | - |
| TR001 | tra | 14 | 0 | 0 | 0 | - | - |
| TR002 | tra | 10 | 0 | 0 | 0 | - | - |
| TR003 | tra | 8 | 0 | 0 | 0 | - | - |
| TR004 | tra | 14 | 0 | 0 | 0 | - | - |
| TR005 | tra | 5 | 0 | 0 | 0 | - | - |
| TR006 | tra | 14 | 1 | 1 | 0 | T-number-L0-ordinary | - |
| TR007 | tra | 8 | 0 | 0 | 0 | - | - |
| TR008 | tra | 8 | 1 | 1 | 0 | T-number-L0-ordinary | - |
| TR009 | tra | 8 | 0 | 0 | 0 | - | - |
| TR010 | tra | 8 | 1 | 1 | 0 | T-number-L0-ordinary | - |
| TR011 | tra | 12 | 0 | 0 | 0 | - | - |
| TR012 | tra | 15 | 0 | 0 | 0 | - | - |
| TR013 | tra | 19 | 1 | 1 | 0 | T-number-L0-ordinary | - |
| TR014 | tra | 7 | 4 | 3 | 1 | T-text-L0-ordinary, A-unicode-decimal-digits, A-predicate-6 | - |
| TR015 | tra | 7 | 2 | 2 | 0 | A-unicode-decimal-digits, A-nfkc-normalize | - |
| TR016 | tra | 5 | 2 | 2 | 0 | T-text-L0-ordinary, A-nfkc-normalize | - |
| TR017 | tra | 8 | 2 | 2 | 0 | T-left-L0-ordinary, T-right-L0-ordinary | - |
| TR018 | tra | 7 | 0 | 0 | 0 | - | - |
| TR019 | tra | 4 | 0 | 0 | 0 | - | - |
| TR020 | tra | 4 | 1 | 1 | 0 | T-text-L0-ordinary | - |
| TR021 | tra | 11 | 0 | 0 | 0 | - | - |
| TR022 | tra | 4 | 1 | 1 | 0 | T-text-L0-ordinary | - |
| TR023 | tra | 11 | 1 | 1 | 0 | T-noun-L0-ordinary | - |
| TR024 | tra | 13 | 3 | 3 | 0 | T-text-L0-ordinary, A-unicode-decimal-digits, A-nfkc-normalize | - |
| TR025 | tra | 13 | 1 | 1 | 0 | M-values-on-error | - |
| TR026 | tra | 12 | 2 | 1 | 1 | M-values-on-error | - |
| TR027 | tra | 16 | 2 | 1 | 1 | M-values-on-error | - |
| TR028 | tra | 12 | 2 | 1 | 1 | M-values-on-error | - |
| TR029 | tra | 21 | 4 | 3 | 1 | T-width-L0-ordinary, M-values-sort, M-values-on-error | - |
| TR030 | tra | 20 | 6 | 5 | 1 | T-matrix-L0-ordinary, T-matrix-L1-ordinary, O-value-before-type, M-matrix-sort, M-matrix-on-error | - |
| TR031 | tra | 22 | 4 | 2 | 2 | M-left-on-error, M-right-on-error | - |
| TR032 | tra | 19 | 2 | 1 | 1 | M-values-on-error | - |
| TR033 | tra | 20 | 3 | 2 | 1 | M-values-sort, M-values-on-error | - |
| TR034 | tra | 26 | 3 | 2 | 1 | M-values-sort, M-values-on-error | - |
| TR035 | tra | 16 | 2 | 1 | 1 | M-values-on-error | - |
| TR036 | tra | 15 | 2 | 1 | 1 | M-values-on-error | - |
| TR037 | tra | 10 | 2 | 1 | 1 | A-predicate-4 | - |
| TR038 | tra | 8 | 2 | 0 | 2 | - | - |
| TR039 | tra | 7 | 0 | 0 | 0 | - | - |
| TR040 | tra | 7 | 0 | 0 | 0 | - | - |
| TR041 | tra | 12 | 3 | 1 | 2 | A-predicate-4 | - |
| TR042 | tra | 12 | 2 | 1 | 1 | A-predicate-4 | - |
| TR043 | tra | 9 | 2 | 0 | 2 | - | - |
| TR044 | tra | 10 | 3 | 1 | 2 | A-predicate-4 | - |
| TR045 | tra | 6 | 0 | 0 | 0 | - | - |
| TR046 | tra | 10 | 1 | 0 | 1 | - | - |
| TR047 | tra | 17 | 2 | 0 | 2 | - | - |
| TR048 | tra | 12 | 1 | 1 | 0 | T-number-L0-ordinary | - |
| TR049 | tra | 28 | 0 | 0 | 0 | - | - |
| TR050 | tra | 24 | 1 | 1 | 0 | B-op3:28:<=->< | - |
| TR051 | tra | 12 | 0 | 0 | 0 | - | - |
| TR052 | tra | 10 | 0 | 0 | 0 | - | - |
| TR053 | tra | 7 | 0 | 0 | 0 | - | - |
| TR054 | tra | 7 | 0 | 0 | 0 | - | - |
| TR055 | tra | 19 | 0 | 0 | 0 | - | - |
| TR056 | tra | 10 | 2 | 0 | 2 | - | - |
| TR057 | tra | 9 | 3 | 1 | 2 | T-text-L0-ordinary | - |
| TR058 | tra | 18 | 4 | 2 | 2 | T-left-L0-ordinary, T-right-L0-ordinary | - |
| TR059 | tra | 29 | 6 | 4 | 2 | T-left-L0-ordinary, T-right-L0-ordinary, M-left-on-error, M-right-on-error | - |
| TR060 | tra | 21 | 2 | 2 | 0 | T-text-L0-ordinary, A-nfkc-normalize | - |

## Gaps still open in candidate-007 (76)

| Task | Mutant | Requirement | Witness args | Reference | Mutant |
|---|---|---|---|---|---|
| DV004 | `O-value-before-type` | type-before-value validation order | `([-4, '1'],)` | raise 'TypeError' | raise 'ValueError' |
| DV004 | `M-values-on-error` | values: no input mutation (error path; contract-only) | `([-1],)` | raise 'ValueError' | raise 'ValueError'; args after: ('tuple', (('list', (('int', '-1'), ('int', '-1'))),)) |
| DV005 | `T-text-L0-ordinary` | text level 0 (str): exact types: ordinary wrong type rejected | `(['a'],)` | raise 'TypeError' | raise 'ValueError' |
| DV006 | `T-text-L0-ordinary` | text level 0 (str): exact types: ordinary wrong type rejected | `(['a'],)` | raise 'TypeError' | raise 'ValueError' |
| DV007 | `B-op4:46:<-><=` | boundary off-by-one: op4:46:<-><= | `(0, 1, 1, 1)` | raise 'IndexError' | return ('list', (('tuple', (('int', '0'), ('int', '0'))),)) |
| DV009 | `M-values-on-error` | values: no input mutation (error path; contract-only) | `([], 1.5)` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('list', (('int', '0'),)), ('float', '1.5'))) |
| DV010 | `T-tokens-L1-ordinary` | tokens level 1 (str): exact types: ordinary wrong type rejected | `(['١', 1],)` | raise 'TypeError' | raise 'ValueError' |
| DV010 | `O-value-before-type` | type-before-value validation order | `([1, 1],)` | raise 'TypeError' | raise 'ValueError' |
| DV010 | `M-tokens-on-error` | tokens: no input mutation (error path; contract-only) | `([],)` | raise 'ValueError' | raise 'ValueError'; args after: ('tuple', (('list', (('str', "''"),)),)) |
| DV010 | `B-num7:26:2->1` | boundary off-by-one: num7:26:2->1 | `(['4', '+'],)` | raise 'ValueError' | raise 'IndexError' |
| DV010 | `B-re10:{0,3}:2:3->2` | boundary off-by-one: re10:{0,3}:2:3->2 | `(['9999'],)` | return ('int', '9999') | raise 'ValueError' |
| DV010 | `B-re10:{0,3}:2:3->4` | boundary off-by-one: re10:{0,3}:2:3->4 | `(['10000'],)` | raise 'ValueError' | return ('int', '10000') |
| DV011 | `T-intervals-L0-ordinary` | intervals level 0 (list): exact types: ordinary wrong type rejected | `((),)` | raise 'TypeError' | return ('list', ()) |
| DV011 | `T-intervals-L1-ordinary` | intervals level 1 (tuple): exact types: ordinary wrong type rejected | `([[1, 2]],)` | raise 'TypeError' | return ('list', (('tuple', (('int', '1'), ('int', '2'))),)) |
| DV011 | `O-value-before-type` | type-before-value validation order | `([(1,), -1],)` | raise 'TypeError' | raise 'ValueError' |
| DV011 | `M-intervals-on-error` | intervals: no input mutation (error path; contract-only) | `([1],)` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('list', (('int', '1'), ('int', '1'))),)) |
| DV011 | `B-num6:35:1->0` | boundary off-by-one: num6:35:1->0 | `([(2, 60), (-3, -1), (10, 100)],)` | return ('list', (('tuple', (('int', '-3'), ('int', '-1'))), ('tuple', (('int', '2'), ('int | return ('list', (('tuple', (('int', '-3'), ('int', '-1'))), ('tuple', (('int', '2'), ('int |
| DV011 | `B-num6:50:1->0` | boundary off-by-one: num6:50:1->0 | `([(2, 60), (-3, -1), (10, 100)],)` | return ('list', (('tuple', (('int', '-3'), ('int', '-1'))), ('tuple', (('int', '2'), ('int | return ('list', (('tuple', (('int', '2'), ('int', '100'))), ('tuple', (('int', '2'), ('int |
| DV011 | `B-num6:62:1->0` | boundary off-by-one: num6:62:1->0 | `([(2, 60), (-3, -1), (10, 100)],)` | return ('list', (('tuple', (('int', '-3'), ('int', '-1'))), ('tuple', (('int', '2'), ('int | return ('list', (('tuple', (('int', '-3'), ('int', '-1'))), ('tuple', (('int', '-3'), ('in |
| DV011 | `B-num6:85:1->0` | boundary off-by-one: num6:85:1->0 | `([(1, 2), (26, 27), (25, 130), (25, 256)],)` | return ('list', (('tuple', (('int', '1'), ('int', '2'))), ('tuple', (('int', '25'), ('int' | return ('list', (('tuple', (('int', '1'), ('int', '2'))), ('tuple', (('int', '25'), ('int' |
| DV012 | `T-text-L0-ordinary` | text level 0 (str): exact types: ordinary wrong type rejected | `(['a'],)` | raise 'TypeError' | raise 'ValueError' |
| TR006 | `T-number-L0-ordinary` | number level 0 (int): exact types: ordinary wrong type rejected | `(-1.5,)` | raise 'TypeError' | raise 'ValueError' |
| TR008 | `T-number-L0-ordinary` | number level 0 (int): exact types: ordinary wrong type rejected | `(-1.5,)` | raise 'TypeError' | raise 'ValueError' |
| TR010 | `T-number-L0-ordinary` | number level 0 (int): exact types: ordinary wrong type rejected | `(-1.5,)` | raise 'TypeError' | raise 'ValueError' |
| TR013 | `T-number-L0-ordinary` | number level 0 (int): exact types: ordinary wrong type rejected | `(-1.5, 2)` | raise 'TypeError' | raise 'ValueError' |
| TR014 | `T-text-L0-ordinary` | text level 0 (str): exact types: ordinary wrong type rejected | `(['a'],)` | raise 'TypeError' | return ('str', "'a'") |
| TR014 | `A-unicode-decimal-digits` | ASCII-only rule: unicode-decimal-digits | `('١',)` | return ('str', "'١'") | return ('str', "'1'") |
| TR014 | `A-predicate-6` | ASCII-only rule: 'char != " "' -> 'not char.isspace()' | `(' \n\n,',)` | return ('str', "' \\n\\n,'") | return ('str', "' \\n,'") |
| TR015 | `A-unicode-decimal-digits` | ASCII-only rule: unicode-decimal-digits | `('١',)` | return ('str', "'١'") | return ('str', "'1'") |
| TR015 | `A-nfkc-normalize` | ASCII-only rule: nfkc-normalize | `('onｅ',)` | return ('str', "'onｅ'") | return ('str', "'one'") |
| TR016 | `T-text-L0-ordinary` | text level 0 (str): exact types: ordinary wrong type rejected | `(['a'],)` | raise 'TypeError' | return ('int', '1') |
| TR016 | `A-nfkc-normalize` | ASCII-only rule: nfkc-normalize | `('a1 Ｅ!',)` | return ('int', '1') | return ('int', '2') |
| TR017 | `T-left-L0-ordinary` | left level 0 (str): exact types: ordinary wrong type rejected | `(['a'], '=')` | raise 'TypeError' | return ('str', "'a='") |
| TR017 | `T-right-L0-ordinary` | right level 0 (str): exact types: ordinary wrong type rejected | `('Ａ', ['a'])` | raise 'TypeError' | return ('str', "'Ａa'") |
| TR020 | `T-text-L0-ordinary` | text level 0 (str): exact types: ordinary wrong type rejected | `(['a'],)` | raise 'TypeError' | return ('str', "'a'") |
| TR022 | `T-text-L0-ordinary` | text level 0 (str): exact types: ordinary wrong type rejected | `(['a'],)` | raise 'TypeError' | return ('list', (('str', "'a'"),)) |
| TR023 | `T-noun-L0-ordinary` | noun level 0 (str): exact types: ordinary wrong type rejected | `(-1, 1)` | raise 'TypeError' | raise 'ValueError' |
| TR024 | `T-text-L0-ordinary` | text level 0 (str): exact types: ordinary wrong type rejected | `(['a'],)` | raise 'TypeError' | return ('str', "'A'") |
| TR024 | `A-unicode-decimal-digits` | ASCII-only rule: unicode-decimal-digits | `('١',)` | return ('str', "'١'") | return ('str', "'1'") |
| TR024 | `A-nfkc-normalize` | ASCII-only rule: nfkc-normalize | `('ǅ',)` | return ('str', "'ǅ'") | return ('str', "'Dž'") |
| TR025 | `M-values-on-error` | values: no input mutation (error path; contract-only) | `([1],)` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('list', (('int', '1'), ('int', '1'))),)) |
| TR026 | `M-values-on-error` | values: no input mutation (error path; contract-only) | `(['x'],)` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('list', (('str', "'x'"), ('str', "'x'"))),)) |
| TR027 | `M-values-on-error` | values: no input mutation (error path; contract-only) | `(['x'],)` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('list', (('str', "'x'"), ('str', "'x'"))),)) |
| TR028 | `M-values-on-error` | values: no input mutation (error path; contract-only) | `(['x'],)` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('list', (('str', "'x'"), ('str', "'x'"))),)) |
| TR029 | `T-width-L0-ordinary` | width level 0 (int): exact types: ordinary wrong type rejected | `([], -1.5)` | raise 'TypeError' | raise 'ValueError' |
| TR029 | `M-values-sort` | values: no input mutation (valid calls) (sort) | `([4, 2], 2)` | return ('list', (('list', (('int', '4'), ('int', '2'))),)) | return ('list', (('list', (('int', '4'), ('int', '2'))),)); args after: ('tuple', (('list', (('int', '2'), ('int', '4'))), ('int', '2'))) |
| TR029 | `M-values-on-error` | values: no input mutation (error path; contract-only) | `([], 0)` | raise 'ValueError' | raise 'ValueError'; args after: ('tuple', (('list', (('int', '0'),)), ('int', '0'))) |
| TR030 | `T-matrix-L0-ordinary` | matrix level 0 (list): exact types: ordinary wrong type rejected | `((),)` | raise 'TypeError' | return ('list', ()) |
| TR030 | `T-matrix-L1-ordinary` | matrix level 1 (list): exact types: ordinary wrong type rejected | `([(1,)],)` | raise 'TypeError' | return ('list', (('list', (('int', '1'),)),)) |
| TR030 | `O-value-before-type` | type-before-value validation order | `([[], None, [1, 2, 3, 4, 5]],)` | raise 'TypeError' | raise 'ValueError' |
| TR030 | `M-matrix-sort` | matrix: no input mutation (valid calls) (sort) | `([[59], [1]],)` | return ('list', (('list', (('int', '59'), ('int', '1'))),)) | return ('list', (('list', (('int', '59'), ('int', '1'))),)); args after: ('tuple', (('list', (('list', (('int', '1'),)), ('list', (('int',  |
| TR030 | `M-matrix-on-error` | matrix: no input mutation (error path; contract-only) | `([1],)` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('list', (('int', '1'), ('int', '1'))),)) |
| TR031 | `M-left-on-error` | left: no input mutation (error path; contract-only) | `([], 3)` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('list', (('int', '0'),)), ('int', '3'))) |
| TR031 | `M-right-on-error` | right: no input mutation (error path; contract-only) | `(3, [])` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('int', '3'), ('list', (('int', '0'),)))) |
| TR032 | `M-values-on-error` | values: no input mutation (error path; contract-only) | `(['x'],)` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('list', (('str', "'x'"), ('str', "'x'"))),)) |
| TR033 | `M-values-sort` | values: no input mutation (valid calls) (sort) | `([4, 2], 0)` | return ('list', (('int', '2'),)) | return ('list', (('int', '2'),)); args after: ('tuple', (('list', (('int', '2'), ('int', '4'))), ('int', '0'))) |
| TR033 | `M-values-on-error` | values: no input mutation (error path; contract-only) | `([], 0)` | raise 'IndexError' | raise 'IndexError'; args after: ('tuple', (('list', (('int', '0'),)), ('int', '0'))) |
| TR034 | `M-values-sort` | values: no input mutation (valid calls) (sort) | `([255, 17], 0, 0)` | return ('list', ()) | return ('list', ()); args after: ('tuple', (('list', (('int', '17'), ('int', '255'))), ('int', '0') |
| TR034 | `M-values-on-error` | values: no input mutation (error path; contract-only) | `([], 1, 0)` | raise 'IndexError' | raise 'IndexError'; args after: ('tuple', (('list', (('int', '0'),)), ('int', '1'), ('int', '0'))) |
| TR035 | `M-values-on-error` | values: no input mutation (error path; contract-only) | `(['x'],)` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('list', (('str', "'x'"), ('str', "'x'"))),)) |
| TR036 | `M-values-on-error` | values: no input mutation (error path; contract-only) | `([],)` | raise 'ValueError' | raise 'ValueError'; args after: ('tuple', (('list', (('int', '0'),)),)) |
| TR037 | `A-predicate-4` | ASCII-only rule: '[0-9]' -> '\d' | `('1٠',)` | raise 'ValueError' | return ('int', '10') |
| TR041 | `A-predicate-4` | ASCII-only rule: '[0-9]' -> '\d' | `('-999999999999,99999999999٩',)` | raise 'ValueError' | return ('tuple', (('int', '-999999999999'), ('int', '999999999999'))) |
| TR042 | `A-predicate-4` | ASCII-only rule: '[0-9]' -> '\d' | `('0.999.99٩',)` | raise 'ValueError' | return ('tuple', (('int', '0'), ('int', '999'), ('int', '999'))) |
| TR044 | `A-predicate-4` | ASCII-only rule: '[0-9]' -> '\d' | `('[0:9٩]',)` | raise 'ValueError' | return ('tuple', (('int', '0'), ('int', '99'))) |
| TR048 | `T-number-L0-ordinary` | number level 0 (int): exact types: ordinary wrong type rejected | `(-1.5,)` | raise 'TypeError' | raise 'ValueError' |
| TR050 | `B-op3:28:<=-><` | boundary off-by-one: op3:28:<=->< | `(0, 1, 0)` | raise 'ValueError' | raise 'IndexError' |
| TR057 | `T-text-L0-ordinary` | text level 0 (str): exact types: ordinary wrong type rejected | `(['a'],)` | raise 'TypeError' | raise 'AttributeError' |
| TR058 | `T-left-L0-ordinary` | left level 0 (tuple): exact types: ordinary wrong type rejected | `([-2, 0, 10], (5, 3, 2, 1))` | raise 'TypeError' | raise 'ValueError' |
| TR058 | `T-right-L0-ordinary` | right level 0 (tuple): exact types: ordinary wrong type rejected | `((2, 0), [-2, 1, 3])` | raise 'TypeError' | raise 'ValueError' |
| TR059 | `T-left-L0-ordinary` | left level 0 (list): exact types: ordinary wrong type rejected | `((0, 256, 3), [])` | raise 'TypeError' | raise 'ValueError' |
| TR059 | `T-right-L0-ordinary` | right level 0 (list): exact types: ordinary wrong type rejected | `([], (59, 32))` | raise 'TypeError' | raise 'ValueError' |
| TR059 | `M-left-on-error` | left: no input mutation (error path; contract-only) | `([], 3)` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('list', (('int', '0'),)), ('int', '3'))) |
| TR059 | `M-right-on-error` | right: no input mutation (error path; contract-only) | `(3, [])` | raise 'TypeError' | raise 'TypeError'; args after: ('tuple', (('int', '3'), ('list', (('int', '0'),)))) |
| TR060 | `T-text-L0-ordinary` | text level 0 (str): exact types: ordinary wrong type rejected | `(['a'],)` | raise 'TypeError' | return ('tuple', (('int', '1'), ('int', '0'), ('int', '0'))) |
| TR060 | `A-nfkc-normalize` | ASCII-only rule: nfkc-normalize | `('ǅ',)` | return ('tuple', (('int', '0'), ('int', '0'), ('int', '1'))) | return ('tuple', (('int', '1'), ('int', '0'), ('int', '1'))) |

## Gaps new in candidate-007 (0)

| Task | Mutant | Requirement | Witness args | Reference | Mutant |
|---|---|---|---|---|---|

## Gaps fixed by candidate-007 (45)

| Task | Mutant | Requirement | Witness args | Reference | Mutant |
|---|---|---|---|---|---|
| DV002 | `A-nfkc-normalize` | ASCII-only rule: nfkc-normalize | `('０１:０２',)` | raise 'ValueError' | return ('int', '62') |
| DV004 | `T-values-L1-ordinary` | values level 1 (int): exact types: ordinary wrong type rejected | `([-1.5],)` | raise 'TypeError' | raise 'ValueError' |
| DV006 | `A-nfkc-normalize` | ASCII-only rule: nfkc-normalize | `('Ａ',)` | raise 'ValueError' | return ('str', "'2'") |
| DV007 | `B-op3:28:<=-><` | boundary off-by-one: op3:28:<=->< | `(0, 0, 1, 0)` | raise 'ValueError' | raise 'IndexError' |
| DV008 | `C-input-fold-lower` | case-sensitivity / stated letter case: input fold-lower | `('A', 'a')` | return ('int', '1') | return ('int', '0') |
| DV008 | `C-input-fold-upper` | case-sensitivity / stated letter case: input fold-upper | `('A', 'a')` | return ('int', '1') | return ('int', '0') |
| DV009 | `T-values-L1-ordinary` | values level 1 (int): exact types: ordinary wrong type rejected | `([1.5], 0)` | raise 'TypeError' | return ('int', '0') |
| DV010 | `A-unicode-decimal-digits` | ASCII-only rule: unicode-decimal-digits | `(['٣'],)` | raise 'ValueError' | return ('int', '3') |
| DV010 | `A-nfkc-normalize` | ASCII-only rule: nfkc-normalize | `(['３'],)` | raise 'ValueError' | return ('int', '3') |
| DV011 | `T-intervals-L2-subclass` | intervals level 2 (int): exact types: subclass rejected | `([(IntChild(0), 1)],)` | raise 'TypeError' | return ('list', (('tuple', (('IntChild', '0'), ('int', '1'))),)) |
| DV011 | `T-intervals-L2-ordinary` | intervals level 2 (int): exact types: ordinary wrong type rejected | `([(1.5, 2)],)` | raise 'TypeError' | return ('list', (('tuple', (('float', '1.5'), ('int', '2'))),)) |
| TR014 | `A-nfkc-normalize` | ASCII-only rule: nfkc-normalize | `(' a  ｂ ',)` | return ('str', "' a ｂ '") | return ('str', "' a b '") |
| TR026 | `T-values-L1-ordinary` | values level 1 (int): exact types: ordinary wrong type rejected | `(['x'],)` | raise 'TypeError' | return ('list', (('str', "'x'"),)) |
| TR027 | `T-values-L1-ordinary` | values level 1 (int): exact types: ordinary wrong type rejected | `(['x'],)` | raise 'TypeError' | return ('list', ()) |
| TR028 | `T-values-L1-ordinary` | values level 1 (int): exact types: ordinary wrong type rejected | `([1.5],)` | raise 'TypeError' | return ('list', (('float', '1.5'),)) |
| TR029 | `T-values-L1-ordinary` | values level 1 (int): exact types: ordinary wrong type rejected | `(['x'], 2)` | raise 'TypeError' | return ('list', (('list', (('str', "'x'"),)),)) |
| TR030 | `T-matrix-L2-ordinary` | matrix level 2 (int): exact types: ordinary wrong type rejected | `([['x']],)` | raise 'TypeError' | return ('list', (('list', (('str', "'x'"),)),)) |
| TR031 | `T-left-L1-ordinary` | left level 1 (int): exact types: ordinary wrong type rejected | `(['x'], [])` | raise 'TypeError' | return ('list', ()) |
| TR031 | `T-right-L1-ordinary` | right level 1 (int): exact types: ordinary wrong type rejected | `([], ['x'])` | raise 'TypeError' | return ('list', ()) |
| TR032 | `T-values-L1-ordinary` | values level 1 (int): exact types: ordinary wrong type rejected | `([1.5],)` | raise 'TypeError' | return ('tuple', (('list', ()), ('list', ()), ('list', (('float', '1.5'),)))) |
| TR033 | `T-values-L1-ordinary` | values level 1 (int): exact types: ordinary wrong type rejected | `(['x'], 0)` | raise 'TypeError' | return ('list', ()) |
| TR034 | `T-values-L1-ordinary` | values level 1 (int): exact types: ordinary wrong type rejected | `(['x'], 0, 0)` | raise 'TypeError' | return ('list', ()) |
| TR035 | `T-values-L1-ordinary` | values level 1 (int): exact types: ordinary wrong type rejected | `(['x'],)` | raise 'TypeError' | return ('int', '0') |
| TR036 | `T-values-L1-ordinary` | values level 1 (int): exact types: ordinary wrong type rejected | `(['x'],)` | raise 'TypeError' | return ('str', "'x'") |
| TR037 | `A-nfkc-normalize` | ASCII-only rule: nfkc-normalize | `('３',)` | raise 'ValueError' | return ('int', '3') |
| TR038 | `A-unicode-decimal-digits` | ASCII-only rule: unicode-decimal-digits | `('٣f',)` | raise 'ValueError' | return ('int', '63') |
| TR038 | `A-nfkc-normalize` | ASCII-only rule: nfkc-normalize | `('３f',)` | raise 'ValueError' | return ('int', '63') |
| TR041 | `A-nfkc-normalize` | ASCII-only rule: nfkc-normalize | `('3,４',)` | raise 'ValueError' | return ('tuple', (('int', '3'), ('int', '4'))) |
| TR041 | `B-re3:{0,11}:2:11->12` | boundary off-by-one: re3:{0,11}:2:11->12 | `('0,1000000000000',)` | raise 'ValueError' | return ('tuple', (('int', '0'), ('int', '1000000000000'))) |
| TR042 | `A-nfkc-normalize` | ASCII-only rule: nfkc-normalize | `('1.２.3',)` | raise 'ValueError' | return ('tuple', (('int', '1'), ('int', '2'), ('int', '3'))) |
| TR043 | `A-unicode-decimal-digits` | ASCII-only rule: unicode-decimal-digits | `('١٠',)` | raise 'ValueError' | return ('int', '2') |
| TR043 | `A-nfkc-normalize` | ASCII-only rule: nfkc-normalize | `('１０',)` | raise 'ValueError' | return ('int', '2') |
| TR044 | `A-unicode-decimal-digits` | ASCII-only rule: unicode-decimal-digits | `('[١:٣]',)` | raise 'ValueError' | return ('tuple', (('int', '1'), ('int', '3'))) |
| TR044 | `A-nfkc-normalize` | ASCII-only rule: nfkc-normalize | `('[１:３]',)` | raise 'ValueError' | return ('tuple', (('int', '1'), ('int', '3'))) |
| TR046 | `A-nfkc-normalize` | ASCII-only rule: nfkc-normalize | `('-１',)` | raise 'ValueError' | return ('int', '-1') |
| TR047 | `C-input-fold-lower` | case-sensitivity / stated letter case: input fold-lower | `('A', 'a', 1)` | return ('int', '-1') | return ('int', '0') |
| TR047 | `C-input-fold-upper` | case-sensitivity / stated letter case: input fold-upper | `('A', 'a', 1)` | return ('int', '-1') | return ('int', '0') |
| TR056 | `A-unicode-decimal-digits` | ASCII-only rule: unicode-decimal-digits | `('#١٢٣٤٥٦',)` | raise 'ValueError' | return ('tuple', (('int', '18'), ('int', '52'), ('int', '86'))) |
| TR056 | `A-nfkc-normalize` | ASCII-only rule: nfkc-normalize | `('#１２３４５６',)` | raise 'ValueError' | return ('tuple', (('int', '18'), ('int', '52'), ('int', '86'))) |
| TR057 | `A-unicode-decimal-digits` | ASCII-only rule: unicode-decimal-digits | `('٣',)` | raise 'ValueError' | return ('str', "'3'") |
| TR057 | `A-nfkc-normalize` | ASCII-only rule: nfkc-normalize | `('Ａ',)` | raise 'ValueError' | return ('str', "'a'") |
| TR058 | `T-left-L1-ordinary` | left level 1 (int): exact types: ordinary wrong type rejected | `((1.5, 0, 0), (0, 0, 0))` | raise 'TypeError' | return ('int', '1') |
| TR058 | `T-right-L1-ordinary` | right level 1 (int): exact types: ordinary wrong type rejected | `((0, 0, 0), (1.5, 0, 0))` | raise 'TypeError' | return ('int', '-1') |
| TR059 | `T-left-L1-ordinary` | left level 1 (int): exact types: ordinary wrong type rejected | `(['x'], [])` | raise 'TypeError' | return ('list', (('str', "'x'"),)) |
| TR059 | `T-right-L1-ordinary` | right level 1 (int): exact types: ordinary wrong type rejected | `([], ['x'])` | raise 'TypeError' | return ('list', (('str', "'x'"),)) |

## Anomalies

- DV009 B-op5:13:<-><= candidate-006: pytest timeout (120.11 s; mutant loops forever) - counted as killed
- DV009 B-op5:13:<-><= candidate-007: pytest timeout (120.11 s; mutant loops forever) - counted as killed
- DV009 B-num7:45:1->0 candidate-006: pytest timeout (120.1 s; mutant loops forever) - counted as killed
- DV009 B-num7:45:1->0 candidate-007: pytest timeout (120.1 s; mutant loops forever) - counted as killed
- TR013 B-num3:25:2->1 candidate-006: pytest timeout (120.11 s; mutant loops forever) - counted as killed
- TR013 B-num3:25:2->1 candidate-007: pytest timeout (120.1 s; mutant loops forever) - counted as killed
- TR021 B-num4:84:1->0 candidate-006: pytest timeout (120.11 s; mutant loops forever) - counted as killed
- TR021 B-num4:84:1->0 candidate-007: pytest timeout (120.11 s; mutant loops forever) - counted as killed
- TR059 B-num6:59:1->0 candidate-006: pytest timeout (120.36 s; mutant loops forever) - counted as killed
- TR059 B-num6:59:1->0 candidate-007: pytest timeout (120.45 s; mutant loops forever) - counted as killed
