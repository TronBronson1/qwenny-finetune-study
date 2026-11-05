lambda text,needle,occurrence: ([i for i in range(len(text)) if text.startswith(needle,i)]+[-1]*occurrence)[occurrence-1]
