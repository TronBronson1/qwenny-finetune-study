"""60 original contracts; candidate targets are derived from separate oracle methods."""
from tasklib import add
import itertools

add("batches","items capacity","int int",
    "items >= 0 and capacity > 0. Return the minimum number of capacity-sized batches needed; zero items needs zero. Invalid values raise ValueError.",
    """if items < 0 or capacity <= 0: raise ValueError("domain")
return items // capacity + (1 if items % capacity else 0)""",
    "lambda items,capacity: (items+capacity-1)//capacity",
    [(0,3),(1,3),(3,3),(4,3),(7,1),(10**30,3)], [((-1,3),"ValueError"),((2,0),"ValueError"),((2,-1),"ValueError"),(("bad",0),"TypeError"),((-1,"bad"),"TypeError")],
    list(itertools.product(range(31),range(1,11))))

add("strip_prefix","text prefix","str str",
    "prefix must be nonempty, otherwise ValueError. Remove exactly one case-sensitive literal prefix if present at the start. Preserve whitespace and Unicode; empty text is valid.",
    """if not prefix: raise ValueError("empty prefix")
if text.startswith(prefix): return text[len(prefix):]
return text""",
    "lambda text,prefix: text.removeprefix(prefix)",
    [("abc","a"),("abc","abc"),("abc","z"),("","a"),("aaaa","a"),("Abc","a"),("ba","a"),(" ab"," "),("éclair","é"),("abc","abcd")],
    [(("abc",""),"ValueError"),(("",""),"ValueError")],
    list(itertools.product(["","a","aa","ab","ba","éa"," a"],["a","aa","b","é"," "])))

add("absolute_distance","left right","int int","Return the nonnegative distance between the two integers.",
    "return left-right if left >= right else right-left",
    "lambda left,right: abs(left-right)",
    [(0,0),(1,0),(0,1),(-3,5),(5,-3),(-8,-2),(10**20,-10**20)],
    extra=list(itertools.product(range(-7,8),repeat=2)))

add("clamp","value low high","int int int","Require low <= high, otherwise ValueError. Return value limited to the inclusive interval [low, high].",
    """if low > high: raise ValueError("bounds")
if value < low: return low
if value > high: return high
return value""",
    "lambda value,low,high: min(max(value,low),high)",
    [(-1,0,5),(0,0,5),(3,0,5),(5,0,5),(6,0,5),(4,2,2),(-5,-4,-2)],
    [((1,3,2),"ValueError")],
    [(v,l,h) for l in range(-2,3) for h in range(l,3) for v in range(-4,5)])

add("parity_label","number","int","Return exactly 'even' for an even integer, otherwise 'odd'. Negative integers follow the same rule.",
    "return 'even' if number % 2 == 0 else 'odd'",
    "lambda number: ('even','odd')[number & 1]",
    [(0,),(1,),(2,),(-1,),(-2,),(10**30+1,)],extra=[(n,) for n in range(-30,31)])

add("factorial","number","int","Require 0 <= number <= 12, otherwise ValueError. Return number factorial as an integer; 0! is 1.",
    """if not 0 <= number <= 12: raise ValueError("domain")
result=1
for factor in range(2,number+1): result*=factor
return result""",
    "lambda number: math.factorial(number)",[(0,),(1,),(2,),(5,),(12,)],
    [((-1,),"ValueError"),((13,),"ValueError")],[(n,) for n in range(13)])

add("digit_sum","number","int","Require number >= 0, otherwise ValueError. Return the sum of its decimal digits; zero returns zero.",
    """if number < 0: raise ValueError("domain")
total=0
while number:
    total+=number%10
    number//=10
return total""",
    "lambda number: sum(map(int,str(number)))",
    [(0,),(7,),(10,),(101,),(999,),(10**30+7,)], [((-1,),"ValueError")],[(n,) for n in range(300)])

add("is_square","number","int","Require number >= 0, otherwise ValueError. Return an exact bool indicating whether number is a perfect square.",
    """if number < 0: raise ValueError("domain")
root=math.isqrt(number)
return root*root == number""",
    "lambda number: any(k*k==number for k in range(number+1))",
    [(0,),(1,),(2,),(4,),(15,),(16,),(17,),(100,)], [((-1,),"ValueError")],[(n,) for n in range(201)])

add("signed_gcd","left right","int int","Return the nonnegative greatest common divisor. gcd(0,0) is 0; input signs do not affect the result.",
    """left,right=abs(left),abs(right)
while right: left,right=right,left%right
return left""",
    "lambda left,right: math.gcd(left,right)",
    [(0,0),(0,8),(8,0),(18,12),(-18,12),(18,-12),(-18,-12),(7,13)],
    extra=list(itertools.product(range(-8,9),repeat=2)))

add("population_count","number","int","Require number >= 0, otherwise ValueError. Return the number of set bits in its binary representation.",
    """if number < 0: raise ValueError("domain")
count=0
while number:
    number &= number-1
    count+=1
return count""",
    "lambda number: bin(number).count('1')",
    [(0,),(1,),(2,),(3,),(255,),(256,),(2**100+1,)], [((-1,),"ValueError")],[(n,) for n in range(256)])

add("leap_year","year","int","Require 1 <= year <= 9999, otherwise ValueError. Return an exact bool under the proleptic Gregorian leap-year rule.",
    """if not 1 <= year <= 9999: raise ValueError("domain")
return year%400 == 0 or (year%4 == 0 and year%100 != 0)""",
    "lambda year: calendar.isleap(year)",
    [(1,),(4,),(1900,),(2000,),(2023,),(2024,),(2100,),(9999,)],
    [((0,),"ValueError"),((10000,),"ValueError")],[(n,) for n in range(1,501)])

add("weekday_offset","day delta","int int","Require 0 <= day <= 6, otherwise ValueError. Return the weekday after adding signed delta with wraparound; weekdays are numbered 0 through 6.",
    """if not 0 <= day <= 6: raise ValueError("domain")
return (day+delta)%7""",
    "lambda day,delta: (datetime.date(2001,1,1)+datetime.timedelta(days=day+delta)).weekday()",
    [(0,0),(0,1),(6,1),(0,-1),(3,14),(3,-14),(6,8)],
    [((-1,0),"ValueError"),((7,0),"ValueError")],list(itertools.product(range(7),range(-20,21))))

add("int_to_base","number base","int int","Require number >= 0 and 2 <= base <= 16, otherwise ValueError. Return the lowercase positional representation without leading zeros, except zero is '0'. Digits above 9 are a through f.",
    """if number < 0 or not 2 <= base <= 16: raise ValueError("domain")
if number == 0: return "0"
digits="0123456789abcdef"
result=""
while number:
    number,remainder=divmod(number,base)
    result=digits[remainder]+result
return result""",
    """def oracle(number,base):
    if number == 0: return "0"
    power=1
    while power*base <= number: power*=base
    digits=[]
    while power:
        digit=number//power
        digits.append("0123456789abcdef"[digit])
        number-=digit*power
        power//=base
    return "".join(digits)""",
    [(0,2),(1,16),(15,16),(16,16),(31,2),(81,3),(255,16),(64,8)],
    [((-1,2),"ValueError"),((2,1),"ValueError"),((2,17),"ValueError")],
    list(itertools.product(range(100),[2,3,8,10,16])))

add("collapse_spaces","text","str","Replace each nonempty run of ASCII space U+0020 with one space. Preserve leading/trailing single spaces, tabs, newlines and all other characters.",
    """result=[]
previous=False
for char in text:
    if char != " " or not previous: result.append(char)
    previous=char == " "
return "".join(result)""",
    "lambda text: re.sub(' +',' ',text)",
    [("",),("a",),("   ",),(" a  b ",),("a\t  b",),("a\n  b",),("é  字",)])

add("reverse_words","text","str","Split on arbitrary Unicode whitespace and return words in reverse order, joined by single ASCII spaces. Empty/all-whitespace input returns the empty string.",
    "return ' '.join(reversed(text.split()))",
    "lambda text: ' '.join(re.findall(r'\\S+',text)[::-1])",
    [("",),("   ",),("one",),("one two three",),(" a\tb\nc ",),("é\u2003字",)])

add("count_vowels","text","str","Return the number of ASCII vowels a,e,i,o,u in either ASCII case. Accented letters and y do not count.",
    """total=0
for char in text:
    if char in "aeiouAEIOU": total+=1
return total""",
    "lambda text: len(re.findall('[aeiouAEIOU]',text))",
    [("",),("AEIOUaeiou",),("rhythm",),("Apple pie",),("éÁy",),("a1 E!",)])

add("interleave_strings","left right","str str","Alternate one character from left, then one from right. Append the remainder when one ends. Do not discard whitespace or Unicode.",
    """result=[]
for index in range(max(len(left),len(right))):
    if index < len(left): result.append(left[index])
    if index < len(right): result.append(right[index])
return "".join(result)""",
    "lambda left,right: ''.join(''.join(p) for p in itertools.zip_longest(left,right,fillvalue=''))",
    [("",""),("a",""),("","b"),("ab","12"),("abc","1"),("a","123"),("é字"," X")])

add("is_palindrome","text","str","Return an exact bool for literal, case-sensitive character palindrome equality. Do not remove punctuation or whitespace; empty input is a palindrome.",
    """for index in range(len(text)//2):
    if text[index] != text[-1-index]: return False
return True""",
    "lambda text: text == text[::-1]",
    [("",),("a",),("aa",),("aba",),("abba",),("ab",),("Aa",),("a a",),("é字é",)])

add("normalize_newlines","text","str","Replace CRLF with one LF and remaining CR with LF; preserve existing LF and other characters.",
    "return text.replace('\\r\\n','\\n').replace('\\r','\\n')",
    "lambda text: re.sub(r'\\r\\n|\\r','\\n',text)",
    [("",),("a",),("\r\n",),("\r",),("\n",),("a\r\nb\rc\nd",),("\r\r\n",)])

add("escape_html","text","str","Escape &, <, >, double quote, and single quote as &amp;, &lt;, &gt;, &quot;, and &#x27; respectively. Do not recognize existing entities; escape their ampersands again.",
    """mapping={"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#x27;"}
return "".join(mapping.get(char,char) for char in text)""",
    "lambda text: html.escape(text,quote=True)",
    [("",),("abc",),("<&>",),("\"'",),("&amp;",),("é <a x='1'>",)])

add("common_prefix","left right","str str","Return the longest literal, case-sensitive common prefix of two strings.",
    """index=0
while index < min(len(left),len(right)) and left[index] == right[index]: index+=1
return left[:index]""",
    "lambda left,right: next((left[:i] for i in range(min(len(left),len(right)),-1,-1) if left[:i]==right[:i]),'')",
    [("",""),("","a"),("abc","abc"),("abc","abd"),("abc","a"),("Ab","ab"),("é字a","é字b")])

add("quote_csv_field","text","str","For a single CSV field, double each double quote and wrap the field in double quotes if it contains comma, CR, LF, or double quote. Also quote the empty field. Otherwise return it unchanged.",
    """if text == "" or any(char in text for char in ',\\r\\n"'):
    return '"'+text.replace('"','""')+'"'
return text""",
    """def oracle(text):
    stream=io.StringIO(newline="")
    csv.writer(stream,lineterminator="\\r\\n").writerow([text])
    return stream.getvalue()[:-2]""",
    [("",),("abc",),("a,b",),('a"b',),("a\rb",),("a\nb",),(" a ",),("é",)])

add("plural_count","number noun","int str","Require number >= 0 and nonempty noun, otherwise ValueError. Return '<number> <noun>' for 1, and append exactly 's' to noun otherwise. This is literal formatting, not English inflection.",
    """if number < 0 or noun == "": raise ValueError("domain")
return str(number)+" "+noun+("" if number==1 else "s")""",
    "lambda number,noun: '{} {}'.format(number,noun if number==1 else noun+'s')",
    [(0,"cat"),(1,"cat"),(2,"cat"),(1,"box"),(2,"box"),(10,"é")],
    [((-1,"cat"),"ValueError"),((1,""),"ValueError")])

add("ascii_upper","text","str","Uppercase only ASCII a-z. Preserve all other characters, including non-ASCII letters.",
    """result=[]
for char in text:
    result.append(chr(ord(char)-32) if "a" <= char <= "z" else char)
return "".join(result)""",
    "lambda text: text.translate(str.maketrans('abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'))",
    [("",),("abcXYZ",),("z-a 9",),("éßı",),("a\nb",)])

add("run_length_encode","values","strs","Return a list of (string, run_length) tuples for consecutive equal strings. Empty input returns []; do not combine separated runs.",
    """result=[]
for value in values:
    if result and result[-1][0] == value: result[-1]=(value,result[-1][1]+1)
    else: result.append((value,1))
return result""",
    "lambda values: [(key,len(list(group))) for key,group in itertools.groupby(values)]",
    [([],),(["a"],),(["a","a","b","a"],),(["","","x"],),(["A","a"],),(["é","é","字"],)])

add("stable_unique","values","ints","Return first occurrences only, preserving input order. Do not mutate the input.",
    """seen=set()
result=[]
for value in values:
    if value not in seen:
        seen.add(value)
        result.append(value)
return result""",
    "lambda values: list(dict.fromkeys(values))",
    [([],),([1],),([2,1,2,3,1],),([0,0,-1,-1],),([3,2,1],)])

add("pairwise_differences","values","ints","Return next minus previous for every adjacent pair. Length zero or one returns []. Do not mutate input.",
    "return [values[i+1]-values[i] for i in range(len(values)-1)]",
    "lambda values: [b-a for a,b in itertools.pairwise(values)]",
    [([],),([4],),([1,4,2],),([3,3],),([-2,-5,1],)])

add("prefix_sums","values","ints","Return inclusive prefix sums of the list, with the same length. Empty input returns []. Do not mutate input.",
    """total=0
result=[]
for value in values:
    total+=value
    result.append(total)
return result""",
    "lambda values: list(itertools.accumulate(values))",
    [([],),([5],),([1,2,3],),([-1,2,-3],),([0,0],)])

add("chunk_list","values width","ints int","Require width > 0, otherwise ValueError. Return consecutive lists of at most width items; keep the final partial chunk. Empty input returns []. Do not mutate input.",
    """if width <= 0: raise ValueError("width")
return [values[i:i+width] for i in range(0,len(values),width)]""",
    """def oracle(values,width):
    result=[]
    current=[]
    for item in values:
        current.append(item)
        if len(current)==width: result.append(current); current=[]
    if current: result.append(current)
    return result""",
    [([],2),([1],2),([1,2,3,4],2),([1,2,3],2),([1,2],1),([1,2],9)],
    [(([1],0),"ValueError"),(([], -1),"ValueError")])

add("transpose","matrix","matrix","Require a rectangular list of lists, otherwise ValueError. Return its transpose as lists. [] and any rectangular matrix with zero columns transpose to []. Do not mutate input.",
    """if not matrix: return []
width=len(matrix[0])
if any(len(row)!=width for row in matrix): raise ValueError("ragged")
return [[matrix[row][col] for row in range(len(matrix))] for col in range(width)]""",
    "lambda matrix: [list(col) for col in zip(*matrix)]",
    [([],),([[]],),([[],[]],),([[1,2],[3,4]],),([[1,2,3]],),([[1],[2],[3]],)],
    [(([[1],[2,3]],),"ValueError")])

add("multiset_intersection","left right","ints ints","Return the multiset intersection, in left-input order: each value occurs at most its count in right. Do not mutate either input.",
    """counts=collections.Counter(right)
result=[]
for value in left:
    if counts[value] > 0:
        result.append(value)
        counts[value]-=1
return result""",
    """def oracle(left,right):
    pool=list(right)
    result=[]
    for value in left:
        if value in pool:
            result.append(value); pool.remove(value)
    return result""",
    [([],[]),([1],[]),([],[1]),([2,1,2,3],[2,2,4]),([1,1,1],[1,1]),([-1,0,-1],[0,-1])])

add("partition_sign","values","ints","Return a tuple (negatives, zeros, positives), each a list preserving original order. Do not mutate input.",
    "return ([x for x in values if x<0],[x for x in values if x==0],[x for x in values if x>0])",
    """def oracle(values):
    groups={-1:[],0:[],1:[]}
    for x in values: groups[(x>0)-(x<0)].append(x)
    return groups[-1],groups[0],groups[1]""",
    [([],),([0],),([-1,2,0,-3,2,0],),([1,2],),([-2,-1],)])

add("remove_at","values index","ints int","Require 0 <= index < len(values), otherwise IndexError (negative indices are forbidden). Return a new list with exactly that item removed. Do not mutate input.",
    """if not 0 <= index < len(values): raise IndexError("index")
return values[:index]+values[index+1:]""",
    "lambda values,index: [value for i,value in enumerate(values) if i!=index]",
    [([1],0),([1,2,3],0),([1,2,3],1),([1,2,3],2),([2,2],1)],
    [(([],0),"IndexError"),(([1],-1),"IndexError"),(([1],1),"IndexError")])

add("bounded_slice","values start stop","ints int int","Require 0 <= start <= len(values) and 0 <= stop <= len(values), otherwise IndexError. Return the half-open slice; start > stop returns []. Do not mutate input.",
    """if not 0 <= start <= len(values) or not 0 <= stop <= len(values): raise IndexError("index")
return values[start:stop]""",
    "lambda values,start,stop: [x for i,x in enumerate(values) if start<=i<stop]",
    [([],0,0),([1,2,3],0,3),([1,2,3],1,2),([1,2,3],2,1),([1,2,3],3,3)],
    [(([1],-1,1),"IndexError"),(([1],0,2),"IndexError")])

add("adjacent_equal_count","values","ints","Return how many adjacent pairs are equal. Runs of length k contribute k-1; empty or one item returns 0. Do not mutate input.",
    "return sum(1 for i in range(1,len(values)) if values[i]==values[i-1])",
    "lambda values: sum(max(0,len(list(g))-1) for _,g in itertools.groupby(values))",
    [([],),([1],),([1,1],),([1,1,1],),([1,2,1],),([1,1,2,2,2],)])

add("lower_median","values","ints","Require nonempty input, otherwise ValueError. Return sorted position (len(values)-1)//2, so even lengths choose the lower middle. Do not mutate input.",
    """if not values: raise ValueError("empty")
ordered=sorted(values)
return ordered[(len(ordered)-1)//2]""",
    "lambda values: statistics.median_low(values)",
    [([1],),([4,1],),([9,1,5],),([9,1,5,3],),([-1,-1,0],)], [(([],),"ValueError")])

add("parse_unsigned","text","str","Require a canonical unsigned decimal literal of 1 through 12 ASCII digits: either '0' or a nonzero digit followed by digits. No signs, whitespace or leading zeros. Invalid syntax/length raises ValueError. Return int.",
    """if re.fullmatch(r"(?:0|[1-9][0-9]{0,11})",text) is None: raise ValueError("syntax")
return int(text)""",
    "lambda text: sum((ord(c)-48)*10**i for i,c in enumerate(reversed(text)))",
    [("0",),("1",),("10",),("999999999999",)],
    [(("",),"ValueError"),(("00",),"ValueError"),(("+1",),"ValueError"),((" 1",),"ValueError"),(("١",),"ValueError"),(("1\n",),"ValueError"),(("1000000000000",),"ValueError")])

add("parse_hex_byte","text","str","Require exactly two ASCII hexadecimal digits, case-insensitive; otherwise ValueError. Return the byte value as int.",
    """if re.fullmatch(r"[0-9a-fA-F]{2}",text) is None: raise ValueError("syntax")
return int(text,16)""",
    "lambda text: '0123456789abcdef'.index(text[0].lower())*16+'0123456789abcdef'.index(text[1].lower())",
    [("00",),("09",),("0a",),("Af",),("FF",),("80",)],
    [(("",),"ValueError"),(("f",),"ValueError"),(("000",),"ValueError"),(("g0",),"ValueError"),((" ff",),"ValueError")])

add("parse_bool_word","text","str","Accept exactly 'true' and 'false' in lowercase. Return exact bool. Any other string raises ValueError.",
    """if text not in ("true","false"): raise ValueError("syntax")
return text == "true" """,
    "lambda text: {'true':True,'false':False}[text]",
    [("true",),("false",)],
    [(("True",),"ValueError"),(("false ",),"ValueError"),(("",),"ValueError"),(("1",),"ValueError")])

add("parse_key_value","text","str","Split on the first literal '='. The key must be nonempty; the value may be empty or contain '='. Preserve all characters. Missing '=' or empty key raises ValueError. Return a (key,value) tuple.",
    """key,separator,value=text.partition("=")
if not separator or not key: raise ValueError("syntax")
return key,value""",
    "lambda text: tuple(text.split('=',1))",
    [("a=b",),("a=",),("a=b=c",),(" a = b ",),("é=字",)],
    [(("a",),"ValueError"),(("=a",),"ValueError"),(("",),"ValueError")])

add("parse_int_pair","text","str","Require two comma-separated signed canonical decimal integers. Each component is at most 12 digits excluding an optional minus; '-0' is permitted. No plus, whitespace or leading zeros except 0. Invalid syntax raises ValueError. Return a tuple of two ints.",
    """part=r"-?(?:0|[1-9][0-9]{0,11})"
if re.fullmatch(part+","+part,text) is None: raise ValueError("syntax")
left,right=text.split(",")
return int(left),int(right)""",
    "lambda text: tuple(int(x) for x in text.partition(',')[::2])",
    [("0,0",),("-0,1",),("-2,3",),("999999999999,-1",)],
    [(("1",),"ValueError"),(("1,2,3",),"ValueError"),(("01,2",),"ValueError"),(("+1,2",),"ValueError"),(("1, 2",),"ValueError"),(("١,2",),"ValueError")])

add("parse_version","text","str","Require exactly three dot-separated canonical nonnegative decimal components, each 0 through 999. No leading zeros except '0', signs, whitespace or Unicode digits. Invalid syntax raises ValueError. Return a tuple of three ints.",
    r"""part=r"(?:0|[1-9][0-9]{0,2})"
if re.fullmatch(part+r"\."+part+r"\."+part,text) is None: raise ValueError("syntax")
return tuple(map(int,text.split(".")))""",
    "lambda text: tuple(sum((ord(c)-48)*10**i for i,c in enumerate(reversed(p))) for p in text.split('.'))",
    [("0.0.0",),("1.2.3",),("999.0.10",)],
    [(("1.2",),"ValueError"),(("1.2.3.4",),"ValueError"),(("01.2.3",),"ValueError"),(("1.2.1000",),"ValueError"),(("1.2.٣",),"ValueError")])

add("parse_binary","text","str","Require 1 through 32 ASCII binary digits, allowing leading zeros. Invalid syntax or length raises ValueError. Return int.",
    """if re.fullmatch(r"[01]{1,32}",text) is None: raise ValueError("syntax")
return int(text,2)""",
    "lambda text: sum((ord(c)-48)*2**i for i,c in enumerate(reversed(text)))",
    [("0",),("1",),("001",),("1010",),("1"*32,)],
    [(("",),"ValueError"),(("2",),"ValueError"),((" 1",),"ValueError"),(("1"*33,),"ValueError")])

add("parse_range","text","str","Require literal syntax '[low:high]' with canonical ASCII decimal endpoints 0 through 99 and low <= high. No spaces/signs/leading zeros except 0. Invalid input raises ValueError. Return the endpoint tuple.",
    r"""part=r"(?:0|[1-9][0-9]?)"
if re.fullmatch(r"\["+part+":"+part+r"\]",text) is None: raise ValueError("syntax")
low,high=map(int,text[1:-1].split(":"))
if low > high: raise ValueError("bounds")
return low,high""",
    "lambda text: tuple(map(int,text[1:-1].partition(':')[::2]))",
    [("[0:0]",),("[0:99]",),("[3:7]",),("[99:99]",)],
    [(("[7:3]",),"ValueError"),(("0:1",),"ValueError"),(("[00:1]",),"ValueError"),(("[0:100]",),"ValueError"),(("[0:1] ",),"ValueError")])

add("path_segments","text","str","Split on literal '/' and discard empty segments only. Preserve '.', '..', backslashes, spaces and all other characters; this is not path normalization.",
    "return [part for part in text.split('/') if part]",
    "lambda text: re.findall('[^/]+',text)",
    [("",),("/",),("//a///b/",),("/./../",),("a\\b/c",),("/ a /字/",)])

add("parse_signed","text","str","Require optional '+' or '-' followed by 1 through 12 ASCII digits. Leading zeros and signed zero are allowed. No whitespace. Invalid syntax/length raises ValueError. Return int.",
    """if re.fullmatch(r"[+-]?[0-9]{1,12}",text) is None: raise ValueError("syntax")
return int(text)""",
    """def oracle(text):
    sign=-1 if text.startswith("-") else 1
    digits=text[1:] if text[:1] in ("+","-") else text
    result=0
    for char in digits: result=result*10+ord(char)-48
    return sign*result""",
    [("0",),("-0",),("+0",),("0012",),("-12",),("+999999999999",)],
    [(("",),"ValueError"),(("+",),"ValueError"),(("--1",),"ValueError"),(("1 ",),"ValueError"),(("١",),"ValueError"),(("1"*13,),"ValueError")])

add("index_of_nth","text needle occurrence","str str int","Require nonempty needle and occurrence >= 1, otherwise ValueError. Return the start index of that occurrence, counting overlapping matches; return -1 if absent.",
    """if not needle or occurrence < 1: raise ValueError("domain")
count=0
for index in range(len(text)-len(needle)+1):
    if text[index:index+len(needle)] == needle:
        count+=1
        if count == occurrence: return index
return -1""",
    "lambda text,needle,occurrence: ([i for i in range(len(text)) if text.startswith(needle,i)]+[-1]*occurrence)[occurrence-1]",
    [("","a",1),("aaaa","aa",1),("aaaa","aa",2),("aaaa","aa",3),("aaaa","aa",4),("abc","abc",1),("abc","x",1),("éé","é",2)],
    [(("abc","",1),"ValueError"),(("abc","a",0),"ValueError")])

add("spreadsheet_column","number","int","Require 1 <= number <= 18278, otherwise ValueError. Return the spreadsheet column label: 1=A, 26=Z, 27=AA, 702=ZZ, 703=AAA, 18278=ZZZ.",
    """if not 1 <= number <= 18278: raise ValueError("domain")
result=""
while number:
    number,remainder=divmod(number-1,26)
    result=chr(65+remainder)+result
return result""",
    """def oracle(number):
    if number<=26: return chr(64+number)
    if number<=702:
        n=number-27
        return chr(65+n//26)+chr(65+n%26)
    n=number-703
    return chr(65+n//676)+chr(65+(n//26)%26)+chr(65+n%26)""",
    [(1,),(26,),(27,),(52,),(702,),(703,),(18278,)],
    [((0,),"ValueError"),((18279,),"ValueError")],[(n,) for n in range(1,1000)])

add("row_major_offset","row column rows columns","int int int int","Require rows > 0 and columns > 0, otherwise ValueError. Then require 0 <= row < rows and 0 <= column < columns, otherwise IndexError. Return row-major flat offset.",
    """if rows <= 0 or columns <= 0: raise ValueError("shape")
if not 0 <= row < rows or not 0 <= column < columns: raise IndexError("index")
return row*columns+column""",
    "lambda row,column,rows,columns: list(itertools.product(range(rows),range(columns))).index((row,column))",
    [(0,0,1,1),(0,2,2,3),(1,0,2,3),(1,2,2,3)],
    [((0,0,0,2),"ValueError"),((0,0,2,0),"ValueError"),((-1,0,2,3),"IndexError"),((2,0,2,3),"IndexError"),((0,3,2,3),"IndexError")])

add("unravel_index","index rows columns","int int int","Require rows > 0 and columns > 0, otherwise ValueError. Then require 0 <= index < rows*columns, otherwise IndexError. Return (row,column) in row-major order.",
    """if rows <= 0 or columns <= 0: raise ValueError("shape")
if not 0 <= index < rows*columns: raise IndexError("index")
return divmod(index,columns)""",
    "lambda index,rows,columns: list(itertools.product(range(rows),range(columns)))[index]",
    [(0,1,1),(0,2,3),(2,2,3),(3,2,3),(5,2,3)],
    [((0,0,2),"ValueError"),((-1,2,3),"IndexError"),((6,2,3),"IndexError")])

add("wrap_index","index length","int int","Require length > 0, otherwise ValueError. Return the canonical wrapped index in range(length), including for negative indices.",
    """if length <= 0: raise ValueError("length")
return index%length""",
    "lambda index,length: divmod(index,length)[1]",
    [(0,1),(3,3),(-1,3),(-4,3),(8,3),(10**20,7)],
    [((0,0),"ValueError"),((0,-1),"ValueError")])

add("seconds_to_hms","seconds","int","Require seconds >= 0, otherwise ValueError. Return (hours,minutes,seconds), without wrapping hours at 24; minutes/seconds are each 0..59.",
    """if seconds < 0: raise ValueError("domain")
hours,remainder=divmod(seconds,3600)
minutes,remaining=divmod(remainder,60)
return hours,minutes,remaining""",
    "lambda seconds: (seconds//3600,(seconds//60)%60,seconds%60)",
    [(0,),(59,),(60,),(3599,),(3600,),(90061,)], [((-1,),"ValueError")])

add("format_cents","cents","int","Return exact decimal currency units with two fractional digits and no grouping/currency symbol. Negative amounts have one leading minus. Avoid floating point; zero is '0.00'.",
    """sign="-" if cents < 0 else ""
whole,fraction=divmod(abs(cents),100)
return f"{sign}{whole}.{fraction:02d}" """,
    """def oracle(cents):
    digits=str(abs(cents)).zfill(3)
    return ("-" if cents<0 else "")+digits[:-2]+"."+digits[-2:]""",
    [(0,),(1,),(-1,),(99,),(100,),(-100,),(12345,),(10**30+1,)])

add("grouped_decimal","number","int","Return decimal integer text grouped from the right in groups of three with underscores. Preserve a leading minus, never add plus or leading zeros.",
    """digits=str(abs(number))
groups=[]
while digits:
    groups.append(digits[-3:]); digits=digits[:-3]
return ("-" if number < 0 else "")+"_".join(reversed(groups))""",
    "lambda number: format(number,'_d')",
    [(0,),(1,),(999,),(1000,),(-1000,),(1234567,),(10**30,)])

add("encode_rgb","red green blue","int int int","Require every component in 0..255, otherwise ValueError. Return exactly seven characters '#rrggbb' using lowercase hexadecimal.",
    """if any(not 0 <= value <= 255 for value in (red,green,blue)): raise ValueError("component")
return f"#{red:02x}{green:02x}{blue:02x}" """,
    "lambda red,green,blue: '#'+bytes([red,green,blue]).hex()",
    [(0,0,0),(255,255,255),(1,2,3),(0,128,255)],
    [((-1,0,0),"ValueError"),((0,256,0),"ValueError"),((0,0,-1),"ValueError")])

add("decode_rgb","text","str","Require '#' followed by exactly six ASCII hexadecimal digits, case-insensitive; otherwise ValueError. Return a tuple of three int components.",
    """if re.fullmatch(r"#[0-9a-fA-F]{6}",text) is None: raise ValueError("syntax")
return tuple(int(text[i:i+2],16) for i in (1,3,5))""",
    "lambda text: tuple(bytes.fromhex(text[1:]))",
    [("#000000",),("#ffffff",),("#010203",),("#00aAFF",)],
    [(("ffffff",),"ValueError"),(("#fff",),"ValueError"),(("#gg0000",),"ValueError"),(("#000000\n",),"ValueError")])

add("make_slug","text","str","Only ASCII letters, digits, space, hyphen and underscore are permitted; other characters raise ValueError. Treat space/hyphen/underscore runs as separators, lowercase letters and join nonempty parts by one hyphen. All-separator input returns ''.",
    """if any(char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -_" for char in text): raise ValueError("character")
parts=re.split(r"[ _-]+",text.strip(" _-"))
return "-".join(parts).lower()""",
    """def oracle(text):
    words=[]
    current=""
    for char in text:
        if char in " _-":
            if current: words.append(current); current=""
        else: current+=char.lower()
    if current: words.append(current)
    return "-".join(words)""",
    [("",),(" --_ ",),("Hello World",),(" A__b--C ",),("X9",)],
    [(("a/b",),"ValueError"),(("é",),"ValueError"),(("a\tb",),"ValueError")])

add("compare_versions","left right","tuple3 tuple3","Each argument must have exactly three nonnegative integer components, otherwise ValueError. Compare lexicographically and return exact int -1, 0, or 1.",
    """if any(value < 0 for value in left+right): raise ValueError("component")
return (left>right)-(left<right)""",
    """def oracle(left,right):
    for a,b in zip(left,right):
        if a<b: return -1
        if a>b: return 1
    return 0""",
    [((0,0,0),(0,0,0)),((1,2,3),(1,2,4)),((1,3,0),(1,2,99)),((2,0,0),(1,99,99))],
    [(((1,2),(1,2,3)),"ValueError"),(((1,-1,0),(1,0,0)),"ValueError")])

add("merge_sorted","left right","ints ints","Require both inputs nondecreasing, otherwise ValueError. Return their sorted merge including all duplicates. Do not mutate either input.",
    """if any(values[i] > values[i+1] for values in (left,right) for i in range(len(values)-1)): raise ValueError("order")
result=[]; i=j=0
while i<len(left) and j<len(right):
    if left[i] <= right[j]: result.append(left[i]); i+=1
    else: result.append(right[j]); j+=1
return result+left[i:]+right[j:]""",
    "lambda left,right: sorted(left+right)",
    [([],[]),([1],[]),([],[1]),([1,3],[2,4]),([1,1,3],[1,2]),([-3,0],[-2,0])],
    [(([2,1],[]),"ValueError"),(([],[1,0]),"ValueError")])

add("count_ascii_categories","text","str","Return a tuple (letters,digits,other) counting ASCII A-Z/a-z, ASCII 0-9, and all remaining characters respectively. Unicode letters/digits belong to other.",
    """letters=digits=other=0
for char in text:
    if "A" <= char <= "Z" or "a" <= char <= "z": letters+=1
    elif "0" <= char <= "9": digits+=1
    else: other+=1
return letters,digits,other""",
    "lambda text: (len(re.findall('[A-Za-z]',text)),len(re.findall('[0-9]',text)),len(re.findall('[^A-Za-z0-9]',text)))",
    [("",),("AbZz09",),("a 1!",),("é١",),("\n\t",)])
