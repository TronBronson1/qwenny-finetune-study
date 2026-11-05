lambda text: (len(re.findall('[A-Za-z]',text)),len(re.findall('[0-9]',text)),len(re.findall('[^A-Za-z0-9]',text)))
