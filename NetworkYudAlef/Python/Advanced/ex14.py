from datetime import datetime
my_date = datetime.now()
print(my_date.isoformat())

# b.

def h (s, SIZE = 8):
    print("len=", len(s))
    for p in [s[i*SIZE: min((i +1)*SIZE, len(s)) ] for i in range(int(len(s) /SIZE + 1))]:
        print(" ".join(["%02X" % int(ord(p[i])) if i < len(p) else "  " for i in range(SIZE)]) +\
              "       " + "".join([p[i] if ord(p[i]) > 31  else "." for i in range(len(p))]))

# the following program creates a hex dump of any text passed onto it, the size indicates how many bytes do you want to
# display in each column of text