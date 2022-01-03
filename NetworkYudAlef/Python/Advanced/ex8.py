def my_sum(lst):

    if len(lst) == 0:
        return

    prev = my_sum(lst[1:])

    return (lst[0] + prev) if prev is not None else (lst[0])

assert my_sum ([1.2,2.3,3.0]) == 6.5

assert my_sum ([7,2,3]) == 12

assert my_sum (['yo','ss','i']) == 'yossi'

assert my_sum ([]) == None

assert my_sum ([[1,4],[2],[4]]) == [1, 4, 2, 4]

assert my_sum ([(1,2),(5,5,6)]) ==(1, 2, 5, 5, 6)