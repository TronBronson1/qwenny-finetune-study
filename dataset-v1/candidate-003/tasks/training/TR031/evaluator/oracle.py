def oracle(left,right):
    pool=list(right)
    result=[]
    for value in left:
        if value in pool:
            result.append(value); pool.remove(value)
    return result
