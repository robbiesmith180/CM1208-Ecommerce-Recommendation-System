codes = "2-1-19-9-3 3-15-4-5-19 1-18-5 5-1-19-25 20-15 2-18-5-1-11"
sections = codes.split()
text = ""
for s in sections:
    nums = s.split("-")
    for n in nums:
        value = int(n)
        ch = chr(value + 64)
        text = text + ch
    text = text + ' '
print(text)