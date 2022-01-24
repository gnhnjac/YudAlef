from random import randint as rand;

def ran():
    plength = rand(10,20);
    letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"];
    numbers = ["1","2","3","4","5","6","7","8","9","0"];
    i = 0;
    password = list();
    while i <= plength:
        or21 = rand(0,1);
        highlow = rand(0,1);
        if or21 == 0:
            posle = rand(0,25)
            if highlow == 0:
                password.append(letters[posle].upper());
            else:
                password.append(letters[posle]);
        else:
            posnu = rand(0,9)
            password.append(numbers[posnu]);
        i+=1;
    passwordfinal = "".join(password);
    print(passwordfinal);
    again = input("again? (y/n) ");
    againl = again.lower();
    if againl == "y":
        ran();
    else:
        return;
ran();