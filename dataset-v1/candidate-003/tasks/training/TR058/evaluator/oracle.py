def oracle(left,right):
    for a,b in zip(left,right):
        if a<b: return -1
        if a>b: return 1
    return 0
