import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, types

def _exact(value, kind):
    if type(value) is not kind:
        raise TypeError('exact built-in type required')

def _check(value, schema):
    if schema in ('int', 'str', 'bytes'):
        _exact(value, {'int': int, 'str': str, 'bytes': bytes}[schema])
    elif schema in ('ints', 'strs', 'matrix', 'pairs', 'commands'):
        _exact(value, list)
        for item in value:
            if schema == 'ints':
                _exact(item, int)
            elif schema == 'strs':
                _exact(item, str)
            elif schema == 'matrix':
                _check(item, 'ints')
            elif schema == 'pairs':
                _check(item, 'pair')
            elif schema == 'commands':
                _exact(item, tuple)
    elif schema in ('pair', 'tuple3'):
        _exact(value, tuple)
        for item in value:
            _exact(item, int)
    elif schema == 'objects':
        _exact(value, tuple)
    elif schema == 'maybe_strs':
        if value is not None:
            _check(value, 'strs')
    elif schema == 'stream':
        if type(value) not in (list, tuple, types.GeneratorType):
            raise TypeError('iterable kind')
    elif schema in ('counts', 'aliases'):
        _exact(value, dict)
        for key, item in value.items():
            _exact(key, str)
            _exact(item, int if schema == 'counts' else str)
    else:
        raise AssertionError(schema)

def _types(values, schemas):
    for value, schema in zip(values, schemas):
        _check(value, schema)
    for value, schema in zip(values, schemas):
        if schema in ('pair', 'tuple3') and len(value) != (2 if schema == 'pair' else 3):
            raise ValueError('tuple shape')
        if schema == 'pairs' and any((len(item) != 2 for item in value)):
            raise ValueError('pair shape')

def grouped_decimal(number):
    _types((number,), ('int',))
    digits = str(int(number))
    groups = []
    while digits:
        groups.append(digits[-3:])
        digits = digits[:-3]
    return ('-' if number < 0 else '') + '_'.join(reversed(groups))
