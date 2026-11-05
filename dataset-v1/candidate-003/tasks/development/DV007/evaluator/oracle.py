lambda row,column,rows,columns: [(r,c) for r,c in [(row-1,column),(row,column+1),(row+1,column),(row,column-1)] if 0<=r<rows and 0<=c<columns]
