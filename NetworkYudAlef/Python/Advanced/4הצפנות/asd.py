import string

msg = "Wkh#dwwdfn#zloo#vwduw#dw#vxqvhw"
key = "309"

def encrypt1(message, key):
	return "".join([chr(ord(x) + int(key[0])) for x in message])

def decrypt1(message, key):
    return "".join([chr(ord(x) - int(key[0])) for x in message])

print(decrypt1(msg,key))

msg2 = "YVxcGVRATVhWXxlOXFhVGUZAWEtBFFZXFWBMXEZQWEAVWVZLW11XXg=="
key = "" # 4 digit key

import base64
def encrypt2(message,key):
    return base64.encodebytes("".join([chr(ord(message[i]) ^ ord(key[i % len(key)])) for i in range(len(message))]).encode())
def decrypt2(message, key):
    message = base64.decodebytes(message.encode()).decode()
    return "".join([chr(ord(message[i]) ^ ord(key[i % len(key)])) for i in range(len(message))])

for i in range(10):
    for j in range(10):
        for k in range(10):
            for m in range(10):
                decoded = decrypt2(msg2,f"{i}{j}{k}{m}")
                if "attack" in decoded:
                    print(decoded)

msg3 = "kth tntTeia0lt a lua1 dtt: ro5 Scasa0 wary"

lst = list(string.ascii_lowercase) + list(string.ascii_uppercase)

import random

def encrypt3(message,key):
    random.seed(key)
    l = list(range(len(message)))
    random.shuffle(l)
    return "".join([message[x] for x in l])

def decrypt3(message, key):
    random.seed(key)
    l = list(range(len(message)))
    random.shuffle(l)
    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]
    # [20, 14, 33, 29, 5, 13, 24, 1, 8, 3, 37, 21, 28, 32, 27, 38, 2, 35, 40, 26, 16, 22, 34, 19, 31, 10, 23, 7, 30, 17, 6, 18, 36, 15, 11, 39, 4, 9, 12, 41, 25, 0]
    # asfdalsk;djf lkearnhfgiuerwyfewrfweropig

    message = list(message)
    real_msg = message.copy()
    j = 0
    for i in l:

        real_msg[i] = message[j]
        j+=1

    return "".join(real_msg)


original = "Hello yossi"

encryped = encrypt3(original,"123")

decryped = decrypt3(encryped,"123")

print(decryped)

# for i in lst:
#     for j in lst:
#         for k in lst:
#
#             key = f"{i}{j}{k}"
#
#             decr = decrypt3(msg3, key)
#
#             if "The" in decr[:3]:
#                 print(key)
#                 print(decr)

# The attack will start on Saturday at 15:00

with open('ex4_cipher.txt', 'r') as f:

    key = {}

    for letter in string.ascii_lowercase:
        key[letter] = []

    text = f.read()

    new_text = list(text)

    longest = 0
    for word in text.split(" "):
        word = word.translate(str.maketrans('', '', string.punctuation)).replace('\n','')
        if len(word) > longest:
            longest = len(word)

    for i in range(longest):

        real_stats = {}
        # real stats
        for letter in string.ascii_uppercase:
            real_stats[letter] = 0

        with open('ex4_dictionary.txt', 'r') as f2:

            for word in f2.readlines():

                word = word.replace('\n','')

                if len(word) < i + 1:
                    continue

                real_stats[word[i]]+=1

        real_sum = sum(real_stats.values())

        for letter in real_stats:

            try:
                real_stats[letter] = (real_stats[letter]/real_sum)*100
            except:
                continue

        #print(real_stats)

        fake_stats = {}

        for letter in string.ascii_uppercase:
            fake_stats[letter] = 0

        for word in text.split(" "):
            word = word.translate(str.maketrans('', '', string.punctuation)).replace('\n','')

            if len(word) < i+1:
                continue
            fake_stats[word[i].upper()]+=1

        fake_sum = sum(fake_stats.values())

        if fake_sum < 100:
            continue

        for letter in fake_stats:
            try:
                fake_stats[letter] = (fake_stats[letter] / fake_sum) * 100
            except:
                continue

        for k in range(len(string.ascii_lowercase)):

            # source_letter = max(fake_stats, key=fake_stats.get).lower()
            # destination_letter = max(real_stats, key=real_stats.get).lower()

            source_letter = sorted(fake_stats.items(), key=(lambda i: i[1]))[-1-k][0].lower()

            destination_letter = sorted(real_stats.items(), key=(lambda i: i[1]))[-1-k][0].lower()

            if fake_stats[source_letter.upper()] == 0.0:
                continue

            key[source_letter].append([destination_letter,fake_stats[source_letter.upper()]])

        # for i in range(len(new_text)):
        #
        #     if new_text[i] == source_letter:
        #
        #         new_text[i] =destination_letter

    print(key)

    save_key = key.copy()
    key_orig = key.copy()

    for letter in key:

        best_positives = 0
        best_letter = ''
        for letter_stats in key[letter]:
            total_positives = 0
            for subletter_stats in key[letter]:
                if subletter_stats[0] == letter_stats[0]:
                    total_positives+=1

            if total_positives > 1 and total_positives > best_positives and total_positives != best_positives:
                best_positives = total_positives
                best_letter = letter_stats[0]

        if best_letter == '':
            max_letter = ''
            max_occurence = 0
            for letter_stats in key[letter]:
                if letter_stats[1] > max_occurence:
                    max_occurence = letter_stats[1]
                    max_letter = letter_stats[0]

            if max_letter == '':
                key[letter] = [letter,0]
            else:
                key[letter] = [max_letter,max_occurence]
        else:

            max_letter = ''
            max_occurence = 0
            for letter_stats in key[letter]:
                if letter_stats[1] > max_occurence:
                    max_occurence = letter_stats[1]
                    max_letter = letter_stats[0]

            best_max_stats = 0
            for letter_stats in key[letter]:
                if letter_stats[0] == best_letter and best_max_stats < letter_stats[1]:
                    best_max_stats = letter_stats[1]

            key[letter] = [best_letter,100,best_positives,best_max_stats,max_letter,max_occurence]

    for letter in key:

        if key[letter][1] == 100:

            found = False
            for subletter in key:

                if key[subletter][1] == 100 and key[letter][0] == key[subletter][0] and letter != subletter:

                    # both letters are sure and they are the same

                    # if prominant letter is less common than twin
                    if key[subletter][2] > key[letter][2]:
                        key[letter] = key[letter][-2:]
                    elif key[subletter][2] < key[letter][2]:

                        key[letter] = key[letter][:2]
                    else:
                        # more partitions for twin
                        if key[subletter][3] > key[letter][3]:
                            key[letter] = key[letter][-2:] # revert to regular check
                        else:
                            key[letter] = key[letter][:2]
                            key[subletter] = key[subletter][-2:]

                    found = True

            if not found:

                key[letter] = key[letter][:2]

    for letter in save_key:

        if key[letter][1] == 100:
            save_key[letter] = key[letter][0]
            continue

        max_letter = ''
        max_occurence = 0
        for letter_stats in save_key[letter]:
            if letter_stats[1] > max_occurence:
                eligable = True
                for keyletter in key:
                    if key[keyletter][0] == letter_stats[0]:
                        if key[keyletter][1] > letter_stats[1]:
                            eligable = False
                            break

                for keyletter in key_orig:
                    for subkeyletter in key_orig[keyletter]:
                        if subkeyletter[0] == letter_stats[0]:

                            if subkeyletter[1] > letter_stats[1]:
                                eligable = False
                                break

                if eligable:
                    max_occurence = letter_stats[1]
                    max_letter = letter_stats[0]

        if max_letter == '':
            save_key[letter] = letter
        else:
            save_key[letter] = max_letter
    save_key['l'] = 'a'
    save_key['s'] = 'i'
    for i in range(len(new_text)):

        for letter in save_key:

            if new_text[i].lower() == letter:
                new_text[i] = save_key[letter]
                break

    print(save_key)
    print("".join(new_text))