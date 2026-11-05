lambda values: sum(max(0,len(list(g))-1) for _,g in itertools.groupby(values))
