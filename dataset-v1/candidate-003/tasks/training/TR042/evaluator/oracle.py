lambda text: tuple(sum((ord(c)-48)*10**i for i,c in enumerate(reversed(p))) for p in text.split('.'))
