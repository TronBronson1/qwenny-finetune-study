lambda row,column,rows,columns: list(itertools.product(range(rows),range(columns))).index((row,column))
