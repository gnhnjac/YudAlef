def what(a, b):אבב
    return sum([abs(i - j) for i, j in zip(a, b)]) / float(len(a))


def useful(x):
    """
    Gets an integer list of value corresponding to the 26 characters of the english alphabet, returns a string with
    the corresponding letters in big case.
    """
    return "".join([chr(ord('A') + item - 1) for item in x ])


def omg(s):
    """
    Returns the integer list parameter with negative numbers filtered out
    """
    return filter(lambda x: x >= 0, s)


def magic(x):
    """
    Reverses string x
    """

    return " ".join(x.split()[::-1])


def v2k(x):
    """
    Turns dict key into dict value and vice versa, limited to unique values for each key.
    """

    return {v: k for (k, v) in x.items()} # v2k Limited to 1<>1 relation between k and v