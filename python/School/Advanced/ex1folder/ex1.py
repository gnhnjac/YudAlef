from sys import argv


with open(argv[1], 'r') as f1:

    with open(argv[2], 'w') as f2:

        for word in f1.read().split(' '):

            f2.write(word + '\n')