lambda text: max([0]+[text[:i].count('(')-text[:i].count(')') for i in range(1,len(text)+1)])
