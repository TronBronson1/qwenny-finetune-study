def oracle(values,width):
    result=[]
    current=[]
    for item in values:
        current.append(item)
        if len(current)==width: result.append(current); current=[]
    if current: result.append(current)
    return result
