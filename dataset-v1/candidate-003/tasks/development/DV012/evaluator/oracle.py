def oracle(text):
    previous=None
    while previous!=text:
        previous=text
        for pair in ("()","[]","{}"): text=text.replace(pair,"")
    return text==""
