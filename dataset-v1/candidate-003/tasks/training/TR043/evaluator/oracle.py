lambda text: sum((ord(c)-48)*2**i for i,c in enumerate(reversed(text)))
