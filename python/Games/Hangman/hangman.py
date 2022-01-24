from random import randint as orgr
import re
try:
    def append():
        choiceapp = ""
        choiceapp = input("Would You Like To Append A List? (y/n) ")
        choiceappl = choiceapp.lower()

        if choiceappl == "y":
            choicemf = input("Which List, Food Or Movies? ")
            choicemfl = choicemf.lower()
            if choicemfl == "movies":
                word = input("Write The Word You Wanna Add, Be Careful: ")
                wordl = word.lower()
                if wordl in movieies:
                    print("That word is already in the list!")
                    append()
                else:
                    with open('movies.txt', 'a') as moviesappend:
                        moviesappend.write("\n" + wordl)
                choiceappa = input("Would You Like To Add Another Word? (y/n) ")
                choiceappal = choiceappa.lower()
                if choiceappal == "y":
                    append()
                if choiceappal == "n":
                    sets()
            if choicemfl == "food":
                word = input("Write The Word You Wanna Add, Be Careful: ")
                wordl = word.lower()
                if wordl in foodies:
                    print("That word is already in the list!")
                    append()
                else:
                    with open('food.txt', 'a') as foodappend:
                        foodappend.write("\n" + wordl)
                choiceappa = input("Would You Like To Add Another Word? (y/n) ")
                choiceappal = choiceappa.lower()
                if choiceappal == "y":
                    append()
                if choiceappal == "n":
                    sets()
            else:
                print("Please write food/movies")
                append()    
        if choiceappl == "n":
            sets()
        else:
            print("Please write y/n")
            append()

    with open('food.txt', 'r') as foody:
        foodies = foody.read()
        foodr = foodies.split('\n')
        food = list()
        food.append(foodr)

    with open('movies.txt', 'r') as moviey:
        movieies = moviey.read()
        movier = movieies.split('\n')
        movies = list()
        movies.append(movier)



    def sets():
        randnumf = orgr(0,len(foodr)-1)
        randnummo = orgr(0,len(movier)-1)
        true1()
        inp = input("Food Or Movies? ")
        inpl = inp.lower()
        if inpl == "food":
            global i
            for i in food:
                global compare
                compare = i[randnumf]
                length = len(i[randnumf])
                global listleng
                listleng = list(length * '_')
                guessm()
        elif inpl == "movies":
            for m in movies:
                compare = m[randnummo]
                length = len(m[randnummo])
                listleng = list(length * '_')
                guessn()
        else:
            print("please enter food or movies.")
            sets()
            
    def true1():
        global true
        true = 1

    def guessn():
        global true
        if true == 1:
            true = 0
            onlyonce()
        else:
            global guessy
            guessy = input("Enter A Letter: ")
            laterm()

    faily = 5

    def onlyonce():
        for position in re.finditer(' ',compare):
            pos = position.end() - 1
            listleng[pos] = ' '
            global listlengfinal
            listlengfinal = " ".join(listleng)   
        print(listlengfinal)
        guessn()
    
    def laterm():
        guessl = guessy.lower()
        if guessl == '':
            guessn()
        elif guessl in compare:
            print("True")
            for position in re.finditer(guessl,compare):
                pos = position.end() - 1
                listleng[pos] = guessl
                listlengfinal = " ".join(listleng)
            print(listlengfinal)
            if not "_" in listlengfinal:
                print("you won! the word was " + compare)
                global faily
                faily = 5
                sets()
            guessn()
        else:
            faily-=1
            fails = str(faily)
            print("that's not right, you have "+fails+" lives left")
            if faily == 0:
                print("you failed :( , the word was " + compare)
                faily = 5
                sets()
            guessn()

    def guessm():
        global true
        if true == 1:
            true = 0
            onlyonce2()
        else:
            global guess
            guess = input("Enter A Letter: ")
            later()

    def onlyonce2():
        for position in re.finditer(' ',compare):
            pos = position.end() - 1
            listleng[pos] = ' '
        listlengfinal = " ".join(listleng)
        print(listlengfinal)
        guessm()

    fail = 5
    def later():
        guessl = guess.lower()
        if guessl == '':
            guessm()
        elif guessl in compare:
            print("True")
            for position in re.finditer(guessl,compare):
                pos = position.end() - 1
                listleng[pos] = guessl
                listlengfinal = " ".join(listleng)
            print(listlengfinal)
            if not "_" in listlengfinal:
                print("you won! the word was " + compare)
                global fail
                fail = 5
                sets()
            guessm()
        else:
            fail-=1
            fails = str(fail)
            print("that's not right, you have "+fails+" lives left")
            if fail == 0:
                print("you failed :( , the word was " + compare)
                fail = 5
                sets()
            guessm()
    append()
except:
    print("error")
append()