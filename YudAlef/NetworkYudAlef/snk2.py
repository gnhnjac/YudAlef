
INT_BITS = 8

# Function to left
# rotate n by d bits
def rotate(n, d):
    # In n<<d, last d bits are 0.
    # To put first 3 bits of n at
    # last, do bitwise or of n<<d
    # with n >>(INT_BITS - d)
    return (n << d) | (n >> (INT_BITS - d))

data = b''

with open('encrypted.png', 'rb') as f:
    data += f.read()
    data = bytearray(data)

print(data)
for i in range(len(data)):
    data[i] = rotate(data[i],4) & 0xFF
    if i % 3 == 0:
        data[i] = ~data[i] & 0xFF
    data[i] ^= 0xBA

data = data[::-1]

with open('decrypted.png','wb') as f:
    f.write(data)