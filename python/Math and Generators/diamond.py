import math

height = int(input("Enter odd height: "))

while height % 2 == 0:

    height = int(input("Enter odd height: "))

for i in range(int(-height/2), math.ceil(height/2)):

    print(" " * abs(i), end="")

    print("*" * (int(height/2-abs(i)+1)+int(height/2-abs(i))))