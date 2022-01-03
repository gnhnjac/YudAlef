from random import randint as random

with open("adjectives.txt", 'r') as adjectives:
    readadj=adjectives.read().replace('\n',' ')
    adjlist = readadj.split(' ')

with open("things.txt",'r') as things:
    readthi=things.read().replace('\n',' ')
    thilist = readthi.split(' ')

def password():
    randadj = random(0,len(adjlist))
    randthi = random(0,len(thilist))
    numbers = ["1","2","3","4","5","6","7","8","9","0"];
    i = 0;
    finalpass =''
    finalpass += adjlist[randadj-1]
    finalpass += ' '
    finalpass += thilist[randthi-1]
    finalpassc = finalpass.title()
    fica = finalpassc.replace(' ','')
    i=0
    while i < 3:
        randnum = random(0,9)
        fica += numbers[randnum]
        i+=1
    print(fica)
    again = input("again? (y/n) ");
    againl = again.lower();
    if againl == "y":
        password();
    else:
        return;
password()