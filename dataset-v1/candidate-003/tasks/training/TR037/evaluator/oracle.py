lambda text: sum((ord(c)-48)*10**i for i,c in enumerate(reversed(text)))
