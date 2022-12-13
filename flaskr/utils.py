def chunketize(l, n=4):
    for i in range(0, len(l), n):
        yield l[i:i + n]
