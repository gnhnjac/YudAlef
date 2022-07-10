import string
import threading


def get_pattern(word):

    pattern = list(word)

    letter_index = 0
    for i in range(len(word)):

        if type(pattern[i]) == str:
            pattern[i] = letter_index

            for j in range(len(word)):

                if word[j] == word[i] and j > i:
                    pattern[j] = letter_index

            letter_index+=1

    return "".join([str(s) for s in pattern])

def apply_word(tmp, orig, cipher):
    for i in range(len(orig)):
        if orig[i] not in tmp[cipher[i]]:
            tmp[cipher[i]] += orig[i]

def merge_possibilities(merge, orig):

    for key in merge:

        orig[key] = get_merged_result(orig[key],merge[key])

def get_merged_result(orig_abc, merge_abc):

    if merge_abc == string.ascii_lowercase:
        return orig_abc

    if merge_abc == '':
        return orig_abc

    if orig_abc == '':
        return merge_abc

    res = ""

    for letter in orig_abc:

        if letter in merge_abc:
            res += letter

    return res

cipherdict = {}

for i in range(len(string.ascii_lowercase)):

    cipherdict[string.ascii_lowercase[i]] = string.ascii_lowercase

final_cypher = {}

for i in range(len(string.ascii_lowercase)):

    final_cypher[string.ascii_lowercase[i]] = ''

def check_word(word):
    word = word.translate(str.maketrans('', '', string.punctuation)).replace('\n', '')

    if word == '':
        return
    with open('ex4_dictionary.txt', 'r') as global_dict:
        dict_data = global_dict.read().split('\n')
        tmp = {}

        for i in range(len(string.ascii_lowercase)):
            tmp[string.ascii_lowercase[i]] = ''

        found = False
        for dict_word in dict_data:

            if get_pattern(dict_word) == get_pattern(word):
                apply_word(tmp, dict_word.lower(), word.lower())
                found = True

        if not found:
            print("WORD: " + word)
            print("NOT FOUND")

        merge_possibilities(tmp, cipherdict)

        for key in cipherdict:

            if len(cipherdict[key]) == 1:
                final_cypher[key] = cipherdict[key][0]

# make dict
with open('ex4_cipher.txt', 'r') as cipher:

    data = cipher.read()
    threads = []

    precent = 0
    for word in data.split(" "):

        t = threading.Thread(target=check_word,args=[word])
        t.start()
        threads.append(t)

        precent += 1
        print("Done: " + str((precent/len(data.split(" "))*100)) + "%")

for thread in threads:
    thread.join()

print(cipherdict)
print(final_cypher)

with open('ex4_cipher.txt', 'r') as f:

    new_text = list(f.read())

    for i in range(len(new_text)):

        for letter in final_cypher:

            if new_text[i].lower() == letter and final_cypher[letter] != '':
                new_text[i] = final_cypher[letter]
                break

    print("".join(new_text))