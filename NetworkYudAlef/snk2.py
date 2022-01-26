
def rotate_left(byte):

    new_byte = 0x0

    one = byte & 0b00000001
    one <<= 1
    two = byte & 0b00000010
    two <<= 1
    three = byte & 0b00000100
    three <<= 1
    four = byte & 0b00001000
    four <<= 1
    five = byte & 0b00010000
    five <<= 1
    six = byte & 0b00100000
    six <<= 1
    seven = byte & 0b01000000
    seven <<= 1
    eight = byte & 0b10000000
    eight <<= 1

    new_byte |= one
    new_byte |= two
    new_byte |= three
    new_byte |= four
    new_byte |= five
    new_byte |= six
    new_byte |= seven
    new_byte |= eight

    return new_byte

data = b''

with open('encrypted.png', 'rb') as f:
    data += f.read()
    data = bytearray(data)

print(data)
for i in range(len(data)):
    data[i] = rotate_left(data[i]) & 0xFF
    data[i] = rotate_left(data[i]) & 0xFF
    data[i] = rotate_left(data[i]) & 0xFF
    data[i] = rotate_left(data[i]) & 0xFF
print("After shift",data)

for i in range(len(data)):
    if i % 3 == 0:
        data[i] = ~data[i] & 0xFF
print("After not",data)

for i in range(len(data)):
    data[i] ^= 0xBA
print("after xor",data)

data = data[::-1]
print("after flip", data)

with open('decrypted.png','wb') as f:
    f.write(data)