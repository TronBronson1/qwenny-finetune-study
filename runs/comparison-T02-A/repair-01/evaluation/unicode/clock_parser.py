def minute_of_day(text):
    if type(text) is not str: raise TypeError
    if len(text) != 5 or text[2] != ":" or not (text[:2]+text[3:]).isdigit(): raise ValueError
    h,m = int(text[:2]),int(text[3:])
    if h > 23 or m > 59: raise ValueError
    return h*60+m
