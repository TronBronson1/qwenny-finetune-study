def oracle(text):
    sign=-1 if text.startswith("-") else 1
    digits=text[1:] if text[:1] in ("+","-") else text
    result=0
    for char in digits: result=result*10+ord(char)-48
    return sign*result
