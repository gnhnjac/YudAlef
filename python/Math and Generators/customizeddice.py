from random import randint as bulbulint
def run():
    try:
        mini = input("Minimum Dice: ")
        minimi = int(mini)
        maxi = input("Maximum Dice: ")
        maximi = int(maxi)
        print(bulbulint(minimi,maximi))
        run()
    except ValueError:
        print("Please Type A Number")
        run()

run()