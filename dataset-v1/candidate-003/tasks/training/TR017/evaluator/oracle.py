lambda left,right: ''.join(''.join(p) for p in itertools.zip_longest(left,right,fillvalue=''))
