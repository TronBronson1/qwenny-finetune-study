def strip_prefix(text, prefix):
    if not isinstance(text, str) or not isinstance(prefix, str):
        raise TypeError
    if prefix == "":
        raise ValueError
    return text[len(prefix):] if text.startswith(prefix) else text
