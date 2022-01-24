from random import randint as bulbulint
def rand():
    first = input("From: ");
    second = input("To: ");
    firsti = int(first);
    secondi = int(second);
    print(bulbulint(firsti,secondi));
    rand();
rand();