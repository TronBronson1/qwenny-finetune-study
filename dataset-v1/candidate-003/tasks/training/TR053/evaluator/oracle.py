def oracle(cents):
    digits=str(abs(cents)).zfill(3)
    return ("-" if cents<0 else "")+digits[:-2]+"."+digits[-2:]
