
def res():
    try:
        askr = input("Whats The Radius Of Your Circle? ");
        askrf = float(askr);
        ask = input("Do You Want To Calculate The Area Or The Circumference? ")
        smallask = ask.lower();

        if smallask == "area" :
            area = askrf * askrf * 3.14;
            areas = str(area);
            print("The Area Of Your Circle Is " + areas);
            res();
    
        if smallask == "circumference" :
            circ = askrf * 6.28;
            circs = str(circ);
            print("The Circumference Of Your Circle Is " + circs);
            res();
    except ValueError:
        res();
res();
