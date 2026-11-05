def oracle(text):
    words=[]
    current=""
    for char in text:
        if char in " _-":
            if current: words.append(current); current=""
        else: current+=char.lower()
    if current: words.append(current)
    return "-".join(words)
