ether = input("Enter ethernet address: ")
if len(list(filter(lambda s: len(s) == 2, ether.split(":")))) == 6:
    print("VALID")
else:
    print("INVALID")