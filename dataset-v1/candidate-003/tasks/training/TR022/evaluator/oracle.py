def oracle(text):
    stream=io.StringIO(newline="")
    csv.writer(stream,lineterminator="\r\n").writerow([text])
    return stream.getvalue()[:-2]
