import socket

sock = socket.socket()
sock.connect(("192.168.0.109", 8576))
print("Connected!")
print(sock.recv(1024))
sock.send(b"help")
print(sock.recv(1024))
# found = False
# for i in range(26):
#     for j in range(33,48):
#         for k in range(10):
#             for r in range(10):
#                 numba = F"{chr(ord('A')+i)}{chr(j)}{str(k)}{str(r)}"
#                 sock.send(numba.encode())
#                 msg = sock.recv(1024)
#                 if b"INCORRECT" not in msg:
#                     print(numba, msg)
#                     found = True
#                     break
#                 else:
#                     print(numba)
#             if found:
#                 break
#         if found:
#             break
#     if found:
#         break

sock.send(b"J.58")
print(sock.recv(1024))
sock.send(b"CONFIRM")
with open("img.jpg", "wb") as f:
    for i in range(13):
        data_len = int(sock.recv(6).decode())
        data = b""
        while len(data) < data_len:
            data += sock.recv(data_len)
        f.write(data)
s1 = "Moshe"
s2 = "Tomer"
l = [ord(a) ^ ord(b) for a,b in zip(s1,s2)]
print(l)
s = ""
for i in l:
    if i == 30:
        s += chr(65)
    elif i == 25:
        s += chr(80)
    elif i == 23:
        s += chr(73)
    elif i == 13:
        s += chr(97)
    elif i == 0:
        s += chr(78)
print(s)
sock.send(b"PNAaI")
print(sock.recv(1024))
sock.send(chr(4).encode())
print(sock.recv(1024))
sock.send(b"CONFIRM")
str_len = 59469
st = b""
while len(st) < str_len:
    st += sock.recv(1)
st = st.decode()

passw = ""
indexes = []
for i in range(1,len(st)-1):
    if 33 <= ord(st[i]) <= 47 and 33 <= ord(st[i-1]) <= 47:
        indexes.append(i)

i = 0
while i < len(indexes)-1:
    subs = ""
    for j in range(indexes[i]+1,indexes[i+1]-1):
        ch = st[j]
        if ord('A') <= ord(ch) <= ord('Z'):
            subs += ch
    passw += subs
    i += 2


print(passw)
sock.send(passw.encode())
print(sock.recv(1024))
sock.send(b"CONFIRM")
print(sock.recv(1024))