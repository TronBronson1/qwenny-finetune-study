def strip_prefix(text, prefix):
    if type(text) is not str or type(prefix) is not str:
        raise TypeError
    if prefix == "":
        raise ValueError
    return text.replace(prefix, "")
