OBJS	= brute.o md5-fast-x86.o
SOURCE	= brute.c
HEADER	= 
OUT	= a.out
CC	 = gcc
FLAGS	 = -g -c -Wall
LFLAGS	 = 

all: $(OBJS)
	$(CC) -g $(OBJS) -o $(OUT) $(LFLAGS)

brute.o: brute.c
	$(CC) $(FLAGS) brute.c

md5-fast-x86.o: md5-fast-x86.S
	$(CC) -c md5-fast-x86.S

clean:
	rm -f $(OBJS) $(OUT)