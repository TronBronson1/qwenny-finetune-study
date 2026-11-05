def oracle(left,right):
    @functools.lru_cache(None)
    def distance(i,j):
        if i==len(left): return len(right)-j
        if j==len(right): return len(left)-i
        if left[i]==right[j]: return distance(i+1,j+1)
        return 1+min(distance(i+1,j),distance(i,j+1),distance(i+1,j+1))
    return distance(0,0)
