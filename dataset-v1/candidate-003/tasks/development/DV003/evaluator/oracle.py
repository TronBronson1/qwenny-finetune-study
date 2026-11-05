def oracle(number):
    thousands=["","M","MM","MMM"]
    hundreds=["","C","CC","CCC","CD","D","DC","DCC","DCCC","CM"]
    tens=["","X","XX","XXX","XL","L","LX","LXX","LXXX","XC"]
    ones=["","I","II","III","IV","V","VI","VII","VIII","IX"]
    return thousands[number//1000]+hundreds[(number//100)%10]+tens[(number//10)%10]+ones[number%10]
