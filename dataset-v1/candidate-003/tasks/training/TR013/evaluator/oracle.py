def oracle(number,base):
    if number == 0: return "0"
    power=1
    while power*base <= number: power*=base
    digits=[]
    while power:
        digit=number//power
        digits.append("0123456789abcdef"[digit])
        number-=digit*power
        power//=base
    return "".join(digits)
