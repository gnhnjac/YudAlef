
def digitsnsum():
    inp = input("Please enter a 5 digits number> ")

    while len(inp) != 5 or not inp.isdecimal():
        inp = input("Please enter a 5 digits number> ")

    print(f'You entered the number: {inp}')
    print(f'The digits of this number are: {"".join(inp[i] + ", " if i+1 < len(inp) else inp[i] for i in range(len(inp)))}')
    print(f'The sum of the digits is: {sum([int(inp[i]) for i in range(len(inp))])}')

digitsnsum()