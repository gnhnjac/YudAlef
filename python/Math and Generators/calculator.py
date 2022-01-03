def calc():
    command = input("Calculator: ")
    i = eval(command)
    print(i)
    again()

def again():
    answer=input("again? (y/n) ")
    answerl = answer.lower()
    if answerl == "y":
        calc()
    else:
        return
calc()