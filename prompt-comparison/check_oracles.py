"""Independent bounded oracles for the demonstration references."""
import itertools
import json
from build_materials import DEMONSTRATIONS, ROOT, write

count = 0
ns = {}
exec(DEMONSTRATIONS[0]['reference'], ns)
for items in range(101):
    for capacity in range(1, 21):
        # Count by consuming batches, independent of the reference formula.
        remaining, expected = items, 0
        while remaining > 0:
            expected += 1
            remaining -= capacity
        assert ns['batches'](items, capacity) == expected
        count += 1
ns = {}
exec(DEMONSTRATIONS[1]['reference'], ns)
strings = [''.join(t) for n in range(4) for t in itertools.product('a Bé', repeat=n)]
prefixes = [''.join(t) for n in range(1, 3) for t in itertools.product('a Bé', repeat=n)]
for text in strings:
    for prefix in prefixes:
        matches = len(text) >= len(prefix) and all(text[i] == c for i, c in enumerate(prefix))
        expected = ''.join(text[i] for i in range(len(prefix), len(text))) if matches else text
        assert ns['strip_prefix'](text, prefix) == expected
        count += 1
write(ROOT / 'ORACLE_RESULTS.json', json.dumps({'bounded_independent_valid_input_checks': count, 'passed': True, 'limits': 'Bounded oracle checks of valid inputs only; exception cases are reviewed and exercised in pytest logs. Same agent authored both checks; not an independent reviewer.'}, indent=2))
print(f'{count} independent bounded oracle checks passed')
