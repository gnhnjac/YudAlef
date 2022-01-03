#Create a program that asks the user to enter their name and their age. Print out a message addressed to them that tells them the year that they will turn 100 years old.
#1Add on to the previous program by asking the user for another number and printing out that many copies of the previous message. (Hint: order of operations exists in Python)
#2Print out that many copies of the previous message on separate lines. (Hint: the string "\n is the same as pressing the ENTER button)
def res():
    try:
        global askname;
        askname = input("What's your name? ");
        askage = input("What's your age? ");
        age = int(askage);
        if age < 0 :
            age = age * -1;
            howmany = 100 - age;
            years = 2019 + howmany;
            if (age > 100 and years > 0) is True:
                yearsstr = str(years);
                print("Hello, " + askname + " you turned 100 years old in " + yearsstr + ".");
                copies = "Hello, " + askname + " you turned 100 years old in " + yearsstr + "." + '\n';
                howmanycopies = input("n u m b e r : ");
                howmanycopiesint = int(howmanycopies);
                print((copies * howmanycopiesint));
                res();
            elif (age > 100 and years < 0) is True:
                yearsstr = str(years);
                print("Hello, " + askname + " you turned 100 years old in " + yearsstr + " Before Count.")
                copies = "Hello, " + askname + " you turned 100 years old in " + yearsstr + " Before Count." + '\n';
                howmanycopies = input("n u m b e r : ");
                howmanycopiesint = int(howmanycopies);
                print((copies * howmanycopiesint));
                res();
            else:
                yearsstr = str(years);
                print("Hello, " + askname + " you will turn 100 years old in " + yearsstr + ".")
                copies = "Hello, " + askname + " you will turn 100 years old in " + yearsstr + "." + '\n';
                howmanycopies = input("n u m b e r : ");
                howmanycopiesint = int(howmanycopies);
                print((copies * howmanycopiesint));
                res();
        
        else:
            howmany = 100 - age;
            years = 2019 + howmany;
            if (age > 100 and years > 0) is True:
                yearsstr = str(years);
                print("Hello, " + askname + " you turned 100 years old in " + yearsstr + ".")
                copies = "Hello, " + askname + " you turned 100 years old in " + yearsstr + "." + '\n';
                howmanycopies = input("n u m b e r : ");
                howmanycopiesint = int(howmanycopies);
                print((copies * howmanycopiesint));
                res();
            elif (age > 100 and years < 0) is True:
                yearsstr = str(years);
                print("Hello, " + askname + " you turned 100 years old in " + yearsstr + " Before Count.")
                copies = "Hello, " + askname + " you turned 100 years old in " + yearsstr + " Before Count." + '\n';
                howmanycopies = input("n u m b e r : ");
                howmanycopiesint = int(howmanycopies);
                print((copies * howmanycopiesint));
                res();
            else:
                yearsstr = str(years);
                print("Hello, " + askname + " you will turn 100 years old in " + yearsstr + ".")
                copies = "Hello, " + askname + " you will turn 100 years old in " + yearsstr + "." + '\n';
                howmanycopies = input("n u m b e r : ");
                howmanycopiesint = int(howmanycopies);
                print((copies * howmanycopiesint));
                res();

    except ValueError:
        error();

def error():
    try:
        askage = input("Please Enter Your Age Correctly: ");
        age = int(askage);
        if age < 0 :
            age = age * -1;
            howmany = 100 - age;
            years = 2019 + howmany;
            if (age > 100 and years > 0) is True:
                yearsstr = str(years);
                print("Hello, " + askname + " you turned 100 years old in " + yearsstr + ".");
                copies = "Hello, " + askname + " you turned 100 years old in " + yearsstr + "." + '\n';
                howmanycopies = input("n u m b e r : ");
                howmanycopiesint = int(howmanycopies);
                print((copies * howmanycopiesint));
                res();
            elif (age > 100 and years < 0) is True:
                yearsstr = str(years);
                print("Hello, " + askname + " you turned 100 years old in " + yearsstr + " Before Count.")
                copies = "Hello, " + askname + " you turned 100 years old in " + yearsstr + " Before Count." + '\n';
                howmanycopies = input("n u m b e r : ");
                howmanycopiesint = int(howmanycopies);
                print((copies * howmanycopiesint));
                res();
            else:
                yearsstr = str(years);
                print("Hello, " + askname + " you will turn 100 years old in " + yearsstr + ".")
                copies = "Hello, " + askname + " you will turn 100 years old in " + yearsstr + "." + '\n';
                howmanycopies = input("n u m b e r : ");
                howmanycopiesint = int(howmanycopies);
                print((copies * howmanycopiesint));
                res();
        
        else:
            howmany = 100 - age;
            years = 2019 + howmany;
            if (age > 100 and years > 0) is True:
                yearsstr = str(years);
                print("Hello, " + askname + " you turned 100 years old in " + yearsstr + ".")
                copies = "Hello, " + askname + " you turned 100 years old in " + yearsstr + "." + '\n';
                howmanycopies = input("n u m b e r : ");
                howmanycopiesint = int(howmanycopies);
                print((copies * howmanycopiesint));
                res();
            elif (age > 100 and years < 0) is True:
                yearsstr = str(years);
                print("Hello, " + askname + " you turned 100 years old in " + yearsstr + " Before Count.")
                copies = "Hello, " + askname + " you turned 100 years old in " + yearsstr + " Before Count." + '\n';
                howmanycopies = input("n u m b e r : ");
                howmanycopiesint = int(howmanycopies);
                print((copies * howmanycopiesint));
                res();
            else:
                yearsstr = str(years);
                print("Hello, " + askname + " you will turn 100 years old in " + yearsstr + ".")
                copies = "Hello, " + askname + " you will turn 100 years old in " + yearsstr + "." + '\n';
                howmanycopies = input("n u m b e r : ");
                howmanycopiesint = int(howmanycopies);
                print((copies * howmanycopiesint));
                res();
    except ValueError:
        error();
res();