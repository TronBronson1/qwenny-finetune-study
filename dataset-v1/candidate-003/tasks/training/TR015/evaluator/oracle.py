lambda text: ' '.join(re.findall(r'\S+',text)[::-1])
