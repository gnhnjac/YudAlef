
asd = {'a': 'e', 'b': 'f', 'c': 'r', 'd': '', 'e': '', 'f': 'b', 'g': '', 'h': 'd', 'i': 'o', 'j': 't', 'k': '', 'l': 'a', 'm': 'l', 'n': 'm', 'o': 's', 'p': 'e', 'q': '', 'r': 's', 's': 'i', 't': 'a', 'u': 'g', 'v': '', 'w': 'c', 'x': 'r', 'y': 'f', 'z': ''}
asd2 = {'a': 'e', 'b': 'c', 'c': 'r', 'd': '', 'e': '', 'f': 'b', 'g': '', 'h': 'd', 'i': 'r', 'j': 't', 'k': '', 'l': 'a', 'm': 'e', 'n': 'm', 'o': 'd', 'p': 'o', 'q': '', 'r': 's', 's': 'i', 't': '', 'u': 'g', 'v': '', 'w': 'c', 'x': 'n', 'y': 'e', 'z': ''}

final = {'a': 'e', 'b': 'p', 'c': 'r', 'd': '', 'e': 'w', 'f': 'b', 'g': '', 'h': 'y', 'i': 'h', 'j': 't', 'k': '', 'l': 'a', 'm': 'l', 'n': 'm', 'o': 'd', 'p': 'o', 'q': 'v', 'r': 's', 's': 'i', 't': 'u', 'u': 'g', 'v': '', 'w': 'c', 'x': 'n', 'y': 'f', 'z': ''}

with open('ex4_cipher.txt', 'r') as f:

    new_text = list(f.read())

    for i in range(len(new_text)):

        for letter in asd:

            if new_text[i].lower() == letter and asd[letter] != '':
                new_text[i] = asd[letter]
                break

    print("".join(new_text))
print('---------------------')
print("2nd option:")
with open('ex4_cipher.txt', 'r') as f:

    new_text = list(f.read())

    for i in range(len(new_text)):

        for letter in final:

            if new_text[i].lower() == letter and final[letter] != '':
                new_text[i] = final[letter]
                break

    print("".join(new_text))