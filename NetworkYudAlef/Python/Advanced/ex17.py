
print(''.join(list(map(lambda x: x*2, 'its cool'))))

print(list(range(int(input("Enter number: ")))[::4]))

def dig_sum(num: int) -> int:
    return sum(list(map(lambda x: int(x), num)))

def slice_lists(lst1, lst2):
    return list(filter(lambda x: x in lst2, lst1))

print(slice_lists([1,2,3,4,5],[1,2,3,6]))

def is_prime(num: int) -> bool:

    return list(filter(lambda x: (num/x).is_integer(), range(2,num))) == []
