"""Author and validate fixed demonstrations; no model calls or settings changes."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SHARED = ('Write one complete pytest file using the exact requested import. Do not implement, '
          'mock, inspect, or edit the function. No dependencies beyond pytest. Return one Python '
          'code block, then a short requirement-to-input mapping and accurate limitations. '
          'Do not claim execution unless you executed the tests. Do not claim exhaustive coverage.')

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')

DEMONSTRATIONS = [
    dict(id='D01', family='integer-ceiling-division', module='batch_count', function='batches',
         spec='batches(items, capacity) accepts only exact built-in integers (reject bool and int subclasses). Validate both types before values. items must be >= 0 and capacity > 0, otherwise ValueError. Return the minimum number of capacity-sized batches needed for items; zero items needs zero batches.',
         reference='''def batches(items, capacity):
    if type(items) is not int or type(capacity) is not int:
        raise TypeError
    if items < 0 or capacity <= 0:
        raise ValueError
    return (items + capacity - 1) // capacity
''',
         values='[(0, 3, 0), (1, 3, 1), (3, 3, 1), (4, 3, 2), (7, 1, 7), (10**30, 3, 333333333333333333333333333334)]',
         invalid='[(True, 3), (False, 3), (IntChild(2), 3), (1.5, 3), ("2", 3), (None, 3), (2, True), (2, False), (2, IntChild(3)), (2, 1.5), (2, "3"), (2, None)]',
         badvalues='[(-1, 3), (2, 0), (2, -1)]', precedence='[("bad", 0), (-1, "bad")]',
         mutants=[('floor', 'return (items + capacity - 1) // capacity', 'return items // capacity', '(1, 3) -> 1'),
                  ('extra_batch', 'return (items + capacity - 1) // capacity', 'return items // capacity + 1', '(3, 3) -> 1'),
                  ('bool_subclass', 'type(items) is not int or type(capacity) is not int', 'not isinstance(items, int) or not isinstance(capacity, int)', '(True, 3) -> TypeError'),
                  ('zero_items', 'items < 0', 'items <= 0', '(0, 3) -> 0'),
                  ('precedence', 'if type(items)', 'if items == -1: raise ValueError\n    if type(items)', '(-1, "bad") -> TypeError')],
         mapping='Return tuples cover zero, partial/exact batches, capacity one, and one large integer. Type tuples isolate each invalid type in both positions. Value tuples isolate negative items and nonpositive capacity. Mixed-invalid tuples check two specified type-before-value situations.',
         limits='Finite cases do not cover all integer pairs or all invalid Python types. The large case checks one exact arithmetic result, not performance. Two precedence witnesses do not prove every validation ordering.'),
    dict(id='D02', family='literal-prefix-removal', module='prefix_tools', function='strip_prefix',
         spec='strip_prefix(text, prefix) accepts only exact built-in strings (reject str subclasses). Validate both types before values. Empty prefix raises ValueError. Remove exactly one case-sensitive literal prefix if present at the start; otherwise return text unchanged. Empty text with nonempty prefix is valid. Whitespace and Unicode are ordinary literal characters.',
         reference='''def strip_prefix(text, prefix):
    if type(text) is not str or type(prefix) is not str:
        raise TypeError
    if prefix == "":
        raise ValueError
    return text[len(prefix):] if text.startswith(prefix) else text
''',
         values='[("abc", "a", "bc"), ("abc", "abc", ""), ("abc", "z", "abc"), ("", "a", ""), ("aaaa", "a", "aaa"), ("Abc", "a", "Abc"), ("ba", "a", "ba"), (" ab", " ", "ab"), ("éclair", "é", "clair"), ("abc", "abcd", "abc")]',
         invalid='[(True, "a"), (1, "a"), (None, "a"), (b"a", "a"), (StrChild("a"), "a"), ("abc", True), ("abc", 1), ("abc", None), ("abc", b"a"), ("abc", StrChild("a"))]',
         badvalues='[("abc", ""), ("", "")]', precedence='[(None, "")]',
         mutants=[('replace_all', 'text[len(prefix):] if text.startswith(prefix) else text', 'text.replace(prefix, "")', '("aaaa", "a") -> "aaa"'),
                  ('case_insensitive', 'text.startswith(prefix)', 'text.lower().startswith(prefix.lower())', '("Abc", "a") -> "Abc"'),
                  ('subclass', 'type(text) is not str or type(prefix) is not str', 'not isinstance(text, str) or not isinstance(prefix, str)', '(StrChild("a"), "a") -> TypeError'),
                  ('empty_text', 'if prefix == "":', 'if prefix == "" or text == "":', '("", "a") -> ""'),
                  ('precedence', 'if type(text)', 'if prefix == "": raise ValueError\n    if type(text)', '(None, "") -> TypeError')],
         mapping='Return tuples check a match, whole match, no match, empty text, one removal, case sensitivity, noninitial occurrence, whitespace, Unicode, and a longer prefix. Type tuples isolate invalid inputs in each position. Value tuples check empty prefix. (None, "") checks one mixed-invalid precedence case.',
         limits='These finite examples are not exhaustive over Unicode, string sizes, invalid types, or combinations of invalid arguments. No performance claim or universal validation-order claim follows.')
]

def suite(d):
    return f'''import pytest
from {d['module']} import {d['function']}

class IntChild(int):
    pass

class StrChild(str):
    pass

@pytest.mark.parametrize("left,right,expected", {d['values']})
def test_returns(left, right, expected):
    assert {d['function']}(left, right) == expected

@pytest.mark.parametrize("left,right", {d['invalid']})
def test_types(left, right):
    with pytest.raises(TypeError):
        {d['function']}(left, right)

@pytest.mark.parametrize("left,right", {d['badvalues']})
def test_values(left, right):
    with pytest.raises(ValueError):
        {d['function']}(left, right)

@pytest.mark.parametrize("left,right", {d['precedence']})
def test_type_precedence(left, right):
    with pytest.raises(TypeError):
        {d['function']}(left, right)
'''

def main():
    evidence = {'python': sys.version, 'pytest': subprocess.check_output([sys.executable, '-m', 'pytest', '--version'], text=True).strip(), 'reviewer': 'Codex; authored and checked locally, no independent human review yet', 'demonstrations': {}}
    for d in DEMONSTRATIONS:
        folder = ROOT / 'demonstrations' / d['id']
        test = suite(d)
        write(folder / 'test_target.py', test)
        write(folder / 'SPEC.md', d['spec'] + '\n\n' + SHARED + '\n')
        answer = '```python\n' + test + '```\n\n' + d['mapping'] + '\n\nLimitations: ' + d['limits'] + '\nI have inspected these cases; this demonstration answer does not claim execution. See the separate check record for actual validation.\n'
        write(folder / 'ANSWER.md', answer)
        cases = [('reference', d['reference'], None)]
        for name, old, new, witness in d['mutants']:
            assert old in d['reference']
            cases.append((name, d['reference'].replace(old, new), witness))
        results = []
        for name, impl, witness in cases:
            target = folder / 'checks' / name
            write(target / (d['module'] + '.py'), impl)
            write(target / 'test_target.py', test)
            p = subprocess.run([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', 'test_target.py'], cwd=target, capture_output=True, text=True, timeout=30)
            write(target / 'pytest.log', p.stdout + p.stderr)
            assert p.returncode == (0 if name == 'reference' else 1), (d['id'], name, p.stdout)
            assert name == 'reference' or ('FAILED test_target.py::test_' in p.stdout and 'ERROR collecting' not in p.stdout)
            results.append({'implementation': name, 'exit_code': p.returncode, 'witness': witness, 'summary': p.stdout.strip().splitlines()[-1]})
        evidence['demonstrations'][d['id']] = results
        write(folder / 'REVIEW.md', '# Review\n\nFamily: ' + d['family'] + '; split: training candidate; revision: 1.\nSource: original locally authored contract, reference and tests. No external source copied.\n\nConcrete tuple results and exception inputs inspected against the contract. Reference execution and all five non-equivalent single-defect mutants checked; logs retained. This is an agent review, not an independent human review. A second reviewer is still needed before admitting these to the training dataset.\n\n' + d['mapping'] + '\n\n' + d['limits'] + '\n')
    write(ROOT / 'CHECK_RESULTS.json', json.dumps(evidence, indent=2))
    prompt_doc = ROOT.parent / '05_FIRST_ALTERATION.md'
    prompt = prompt_doc.read_text(encoding='utf-8').split('## Candidate system prompt v1\n\n')[1].split('\n## Controlled use')[0].strip()
    write(ROOT / 'SYSTEM_PROMPT.txt', prompt + '\n')
    demos = '\n\n'.join('Demonstration ' + d['id'] + '\nSpecification: ' + d['spec'] + '\n\nCorrect answer:\n' + (ROOT / 'demonstrations' / d['id'] / 'ANSWER.md').read_text(encoding='utf-8') for d in DEMONSTRATIONS)
    write(ROOT / 'DEMONSTRATIONS.md', demos)
    write(ROOT / 'SHARED_INSTRUCTIONS.txt', SHARED + '\n')
    manifest = [{'id': d['id'], 'family': d['family'], 'split': 'training-candidate', 'revision': 1} for d in DEMONSTRATIONS]
    write(ROOT / 'split_manifest.json', json.dumps(manifest, indent=2))
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*') if p.is_file() and p.suffix in ('.md', '.txt', '.py', '.json') and p.name != 'SHA256.json' and '__pycache__' not in str(p)}
    write(ROOT / 'SHA256.json', json.dumps(hashes, indent=2))
    print(json.dumps(evidence, indent=2))

if __name__ == '__main__':
    main()
