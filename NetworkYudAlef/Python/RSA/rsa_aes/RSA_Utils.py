import random


def msg_to_num(msg):

    # new_msg = 0
    #
    # for byte in msg:
    #     new_msg += new_msg*256 + int(byte) ^ random.randrange(0,256)
    #
    # return new_msg
    return msg

def num_to_msg(msg):
    # new_msg = ''
    #
    # for byte in msg:
    #     new_msg += byte ^ random.randrange(0, 256)
    #
    # return new_msg
    return str(msg)

def get_euler(p,q):
    return (p-1)*(q-1)

def get_n(p,q):
    return p*q

def are_strangers(n1,n2):
    shared = []
    for i in range(1,max(n1,n2)):
        if n1 % i == 0 and n2 % i == 0:
            shared.append(i)
    return shared == [1]

def get_e(euler):
    while True:
        num = random.randrange(2,euler)
        if are_strangers(num,euler):
            return num

def get_d(e, euler):
    return (1/e)%euler

def encrypt(m, e, n):
    """
    :param m: m is the original message
    :param e: e is the other side's public key
    :param n: n is the prime multiplicative
    :return: encrypted message
    """
    return pow(msg_to_num(m),e,n)

def decrypt(c,d,n):
    """
    :param c: c is encrypted message using public key 'e'
    :param d: d is our private key
    :param n: n is the prime multiplicative
    :return: decrypted message
    """
    print(type(c))
    print(c)
    print(type(d))
    print(d)
    print(type(n))
    print(n)
    return num_to_msg((c**d)%n)