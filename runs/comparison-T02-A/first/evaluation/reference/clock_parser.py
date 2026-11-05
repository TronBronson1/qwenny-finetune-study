def minute_of_day(text):
    if type(text) is not str: raise TypeError
    if len(text) != 5 or text[2] != ":" or any(c not in "0123456789" for c in text[:2]+text[3:]): raise ValueError
    h,m = int(text[:2]),int(text[3:])
    if h > 23 or m > 59: raise ValueError
    return h*60+m
