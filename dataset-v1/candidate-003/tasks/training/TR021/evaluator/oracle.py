lambda left,right: next((left[:i] for i in range(min(len(left),len(right)),-1,-1) if left[:i]==right[:i]),'')
