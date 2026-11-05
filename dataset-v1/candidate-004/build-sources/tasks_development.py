"""Development families. Rotation and clock parsing were already exposed."""
from tasklib import add
import itertools

add("rotate_right","values steps","objects int",
    "values must be an exact built-in tuple; elements may be arbitrary objects. Rotate right by signed steps, wrapping modulo length; negative steps rotate left. Empty input returns (). Preserve element identities and order; do not mutate elements.",
    """if not values: return ()
amount=steps%len(values)
return values[-amount:]+values[:-amount] if amount else values[:]""",
    """def oracle(values,steps):
    queue=collections.deque(values)
    queue.rotate(steps)
    return tuple(queue)""",
    [((),0),((),4),((1,),-9),((1,2,3),0),((1,2,3),1),((1,2,3),-1),((1,2,3),7),((1,1,2),2),(([1],{"k":2}),1)],
    extra_tests="""def test_identity_and_no_element_mutation():
    first=[1]
    second={"k":2}
    third=object()
    values=(first,second,third)
    result=rotate_right(values,1)
    assert type(result) is tuple
    assert result[0] is third
    assert result[1] is first
    assert result[2] is second
    assert first == [1]
    assert second == {"k":2}
""")

add("minute_of_day","text","str",
    "Accept exactly five ASCII characters HH:MM, hours 00..23 and minutes 00..59. Return hour*60+minute as an exact int. No trimming, signs, Unicode digits or extra characters. All malformed strings raise ValueError.",
    """if re.fullmatch(r"[0-9]{2}:[0-9]{2}",text) is None: raise ValueError("syntax")
hour,minute=map(int,text.split(":"))
if hour > 23 or minute > 59: raise ValueError("time")
return hour*60+minute""",
    "lambda text: int(text[:2])*60+int(text[3:])",
    [("00:00",),("00:01",),("01:00",),("12:34",),("23:59",)],
    [(("24:00",),"ValueError"),(("23:60",),"ValueError"),(("1:00",),"ValueError"),(("00:0",),"ValueError"),(("00-00",),"ValueError"),((" 00:00",),"ValueError"),(("00:00\n",),"ValueError"),(("٠٠:٠٠",),"ValueError")],
    [(f"{h:02}:{m:02}",) for h in range(24) for m in range(60)])

add("roman_encode","number","int",
    "Require 1 <= number <= 3999, otherwise ValueError. Return canonical uppercase Roman numerals with subtractive IV, IX, XL, XC, CD, CM.",
    """if not 1 <= number <= 3999: raise ValueError("domain")
result=""
for amount,symbol in [(1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),(100,"C"),(90,"XC"),(50,"L"),(40,"XL"),(10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I")]:
    while number >= amount:
        result+=symbol
        number-=amount
return result""",
    """def oracle(number):
    thousands=["","M","MM","MMM"]
    hundreds=["","C","CC","CCC","CD","D","DC","DCC","DCCC","CM"]
    tens=["","X","XX","XXX","XL","L","LX","LXX","LXXX","XC"]
    ones=["","I","II","III","IV","V","VI","VII","VIII","IX"]
    return thousands[number//1000]+hundreds[(number//100)%10]+tens[(number//10)%10]+ones[number%10]""",
    [(1,),(4,),(9,),(40,),(90,),(400,),(900,),(1994,),(3999,)],
    [((0,),"ValueError"),((4000,),"ValueError")],[(n,) for n in range(1,4000)])

add("xor_checksum","values","ints",
    "Require every item 0..255, otherwise ValueError. Return bitwise XOR of all items as int; empty input returns 0. Do not mutate input.",
    """if any(not 0 <= value <= 255 for value in values): raise ValueError("byte")
result=0
for value in values: result ^= value
return result""",
    "lambda values: functools.reduce(operator.xor,values,0)",
    [([],),([0],),([255],),([1,2,3],),([5,5],),([128,1,128],)],
    [(([-1],),"ValueError"),(([256],),"ValueError")])

add("parenthesis_depth","text","str",
    "Only '(' and ')' are permitted. Require a balanced sequence with no premature closing parenthesis, otherwise ValueError. Return maximum nesting depth as int; empty input returns 0.",
    """if any(char not in "()" for char in text): raise ValueError("character")
depth=maximum=0
for char in text:
    depth+=1 if char=="(" else -1
    if depth < 0: raise ValueError("unbalanced")
    maximum=max(maximum,depth)
if depth: raise ValueError("unbalanced")
return maximum""",
    "lambda text: max([0]+[text[:i].count('(')-text[:i].count(')') for i in range(1,len(text)+1)])",
    [("",),("()",),("(())",),("()()",),("(()(()))",)],
    [(("(",),"ValueError"),((")",),"ValueError"),((")(",),"ValueError"),(("(a)",),"ValueError")])

add("keypad_encode","text","str",
    "Accept only uppercase ASCII A-Z; other characters raise ValueError. Map to telephone keypad digits ABC=2, DEF=3, GHI=4, JKL=5, MNO=6, PQRS=7, TUV=8, WXYZ=9. Empty input returns ''.",
    """if any(not "A" <= char <= "Z" for char in text): raise ValueError("character")
mapping={char:str(digit) for digit,group in enumerate(["ABC","DEF","GHI","JKL","MNO","PQRS","TUV","WXYZ"],2) for char in group}
return "".join(mapping[char] for char in text)""",
    "lambda text: text.translate(str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZ','22233344455566677778889999'))",
    [("",),("ABC",),("HELLO",),("PQRS",),("WXYZ",),("ABCDEFGHIJKLMNOPQRSTUVWXYZ",)],
    [(("abc",),"ValueError"),(("A B",),"ValueError"),(("É",),"ValueError")])

add("grid_neighbors","row column rows columns","int int int int",
    "Require positive rows/columns, otherwise ValueError; then require an in-bounds cell, otherwise IndexError. Return in-bounds orthogonal neighbor (row,column) tuples in up, right, down, left order. Do not include the original cell.",
    """if rows <= 0 or columns <= 0: raise ValueError("shape")
if not 0 <= row < rows or not 0 <= column < columns: raise IndexError("cell")
result=[]
if row > 0: result.append((row-1,column))
if column+1 < columns: result.append((row,column+1))
if row+1 < rows: result.append((row+1,column))
if column > 0: result.append((row,column-1))
return result""",
    "lambda row,column,rows,columns: [(r,c) for r,c in [(row-1,column),(row,column+1),(row+1,column),(row,column-1)] if 0<=r<rows and 0<=c<columns]",
    [(0,0,1,1),(0,0,2,3),(1,1,3,3),(2,2,3,3),(0,1,1,3),(1,0,3,1)],
    [((0,0,0,1),"ValueError"),((-1,0,2,2),"IndexError"),((2,0,2,2),"IndexError")])

add("edit_distance","left right","str str",
    "Return Levenshtein distance with insertion, deletion and substitution cost 1; equal characters cost 0. Compare literal Unicode characters case-sensitively.",
    """previous=list(range(len(right)+1))
for i,a in enumerate(left,1):
    current=[i]
    for j,b in enumerate(right,1):
        current.append(min(current[-1]+1,previous[j]+1,previous[j-1]+(a!=b)))
    previous=current
return previous[-1]""",
    """def oracle(left,right):
    @functools.lru_cache(None)
    def distance(i,j):
        if i==len(left): return len(right)-j
        if j==len(right): return len(left)-i
        if left[i]==right[j]: return distance(i+1,j+1)
        return 1+min(distance(i+1,j),distance(i,j+1),distance(i+1,j+1))
    return distance(0,0)""",
    [("",""),("","abc"),("abc",""),("cat","cat"),("cat","cut"),("ab","ba"),("kitten","sitting"),("é","e")],
    extra=list(itertools.product(["","a","b","ab","ba","abc"],repeat=2)))

add("lower_bound","values target","ints int",
    "Require values nondecreasing, otherwise ValueError. Return the first insertion position that keeps target before all equal values (bisect-left behavior). Do not mutate input.",
    """if any(values[i]>values[i+1] for i in range(len(values)-1)): raise ValueError("order")
low,high=0,len(values)
while low<high:
    middle=(low+high)//2
    if values[middle]<target: low=middle+1
    else: high=middle
return low""",
    "lambda values,target: sum(value<target for value in values)",
    [([],0),([1],0),([1],1),([1],2),([1,2,2,4],2),([1,2,2,4],3),([-3,-1,0],-4)],
    [(([2,1],1),"ValueError")])

add("rpn_evaluate","tokens","strs",
    "Require 1..32 tokens forming one reverse-Polish expression. Integers use optional minus and canonical 1..4 ASCII digits (zero and '-0' allowed). Operators are '+', '-', '*'. Insufficient operands, extra operands, invalid tokens/length raise ValueError. Return exact int; do not mutate tokens.",
    """if not 1 <= len(tokens) <= 32: raise ValueError("length")
stack=[]
for token in tokens:
    if token in ("+","-","*"):
        if len(stack)<2: raise ValueError("arity")
        right=stack.pop(); left=stack.pop()
        stack.append({"+":operator.add,"-":operator.sub,"*":operator.mul}[token](left,right))
    elif re.fullmatch(r"-?(?:0|[1-9][0-9]{0,3})",token):
        stack.append(int(token))
    else: raise ValueError("token")
if len(stack)!=1: raise ValueError("arity")
return stack[0]""",
    """def oracle(tokens):
    def parse(index):
        token=tokens[index]
        if token not in ("+","-","*"): return int(token),index-1
        right,index=parse(index-1)
        left,index=parse(index)
        return {"+":lambda:left+right,"-":lambda:left-right,"*":lambda:left*right}[token](),index
    value,index=parse(len(tokens)-1)
    assert index==-1
    return value""",
    [(["0"],),(["-0"],),(["2","3","+"],),(["2","3","-"],),(["2","3","4","*","+"],),(["-2","3","*"],)],
    [(([],),"ValueError"),((["+"],),"ValueError"),((["1","2"],),"ValueError"),((["01"],),"ValueError"),((["1","/"],),"ValueError"),((["1"]*33,),"ValueError")])

add("interval_union","intervals","pairs",
    "Each pair is (low,high) with low < high, otherwise ValueError. Return sorted nonoverlapping half-open interval pairs covering the union; merge overlaps and touching intervals. Input order is arbitrary. Do not mutate input.",
    """if any(low>=high for low,high in intervals): raise ValueError("interval")
result=[]
for low,high in sorted(intervals):
    if result and low<=result[-1][1]: result[-1]=(result[-1][0],max(high,result[-1][1]))
    else: result.append((low,high))
return result""",
    """def oracle(intervals):
    cells=sorted({x for low,high in intervals for x in range(low,high)})
    result=[]
    for cell in cells:
        if result and result[-1][1]==cell: result[-1]=(result[-1][0],cell+1)
        else: result.append((cell,cell+1))
    return result""",
    [([],),([(1,3)],),([(3,5),(1,3)],),([(1,5),(2,3)],),([(1,2),(4,6)],),([(-3,0),(-1,2)],)],
    [(([(1,1)],),"ValueError"),(([(2,1)],),"ValueError"),(([(1,2,3)],),"ValueError")])

add("balanced_brackets","text","str",
    "Only (), [], {} characters are permitted; other characters raise ValueError. Return exact bool for correctly nested and matched brackets. Empty input is balanced; mismatches/unclosed brackets return False.",
    """if any(char not in "()[]{}" for char in text): raise ValueError("character")
stack=[]
matches={")":"(","]":"[","}":"{"}
for char in text:
    if char in "([{": stack.append(char)
    elif not stack or stack.pop()!=matches[char]: return False
return not stack""",
    """def oracle(text):
    previous=None
    while previous!=text:
        previous=text
        for pair in ("()","[]","{}"): text=text.replace(pair,"")
    return text=="" """,
    [("",),("()",),("([]{})",),("([)]",),("(",),("]",),("}{",),("[](){}",)],
    [(("(a)",),"ValueError"),((" ",),"ValueError")])
