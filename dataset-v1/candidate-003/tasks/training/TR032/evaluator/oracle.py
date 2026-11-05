def oracle(values):
    groups={-1:[],0:[],1:[]}
    for x in values: groups[(x>0)-(x<0)].append(x)
    return groups[-1],groups[0],groups[1]
