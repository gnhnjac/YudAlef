
i = 0.0

while (i < 5):

    ij = round(i,1)

    if str(ij)[2] == '0':
        ij = round(i)

    print(ij)
    i += 0.1