from math import sqrt

iterations = 10000000

sum = 0

pivot = 1

for i in range(0,iterations):

    sum += 1 / (pivot * pivot)
    pivot+=1

sum *= 6

sum = sqrt(sum)

print(sum)