#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <time.h>
#include <math.h>

/* Function prototypes */

#define BLOCK_LEN 64  // In bytes
#define STATE_LEN 4  // In words

void md5_hash(const uint8_t message[], size_t len, uint32_t hash[static STATE_LEN]);

extern void md5_compress(const uint8_t block[static BLOCK_LEN], uint32_t state[static STATE_LEN]);

void to_hex(char* dest, const uint8_t* values, size_t val_len);

uint32_t *hex_to_md5_little(const char *hex);

uint32_t hex2int(const char *hex);

int getNum(char ch);

int main(int argc, char **argv) {
    if (argc < 3)
        printf("Format must be: brute.c [MINRANGE] [MAXRANGE]");

    unsigned long minrange = (unsigned long)atoi(argv[1]);
    unsigned long maxrange = (unsigned long)atoi(argv[2]);
    uint32_t *desiredhash = hex_to_md5_little("EC9C0F7EDCC18A98B1F31853B1813301");
    char *number = malloc(20 + 1);

    for (unsigned long i = minrange; i < maxrange; i++)
    {
        sprintf(number, "%lu", i);
        uint32_t hash[STATE_LEN];
		md5_hash((uint8_t *)number, strlen(number), hash);
        if (memcmp(hash, desiredhash, 16) == 0)
        {
                printf("%lu", i);
                free(number);
                free(desiredhash);
                return 0;
        }
    }
    free(number);
    free(desiredhash);
	return 1;
}

int getNum(char ch)
{
    int num = 0;
    if (ch >= '0' && ch <= '9') {
        num = ch - 0x30;
    }
    else {
        switch (ch) {
        case 'A':
        case 'a':
            num = 10;
            break;
        case 'B':
        case 'b':
            num = 11;
            break;
        case 'C':
        case 'c':
            num = 12;
            break;
        case 'D':
        case 'd':
            num = 13;
            break;
        case 'E':
        case 'e':
            num = 14;
            break;
        case 'F':
        case 'f':
            num = 15;
            break;
        default:
            num = 0;
        }
    }
    return num;
}

//function : hex2int
//this function will return integer value against
//hexValue - which is in string format

uint32_t hex2int(const char *hex)
{   

    size_t len = strlen(hex);
    uint32_t res = 0;
    for (int i = 0; i < len; i++)
    {

        res += getNum(hex[len-1-i]) * pow(16, i);

    }

    return res;
}

void big_to_little(uint32_t *num)
{
    uint32_t before = *num;
    *num = ((before>>24)&0xff) | // move byte 3 to byte 0
                    ((before<<8)&0xff0000) | // move byte 1 to byte 2
                    ((before>>8)&0xff00) | // move byte 2 to byte 1
                    ((before<<24)&0xff000000); // byte 0 to byte 3

}

uint32_t *hex_to_md5_little(const char *hex)
{

    uint32_t *resbuff = malloc(4*sizeof(uint32_t *));

    for (int i = 0; i < 4; i++)
    {
        char *buffer = (char *)malloc(8 + 1);
        memcpy(buffer, hex + 8*i, 8);
        *(buffer + 8) = '\x0';
        *(resbuff + i) = hex2int(buffer);
        big_to_little(resbuff + i);
        free(buffer);
    }

    return resbuff;
}

/* Full message hasher */

void md5_hash(const uint8_t message[], size_t len, uint32_t hash[static STATE_LEN]) {
	hash[0] = UINT32_C(0x67452301);
	hash[1] = UINT32_C(0xEFCDAB89);
	hash[2] = UINT32_C(0x98BADCFE);
	hash[3] = UINT32_C(0x10325476);
	
	#define LENGTH_SIZE 8  // In bytes
	
	size_t off;
	for (off = 0; len - off >= BLOCK_LEN; off += BLOCK_LEN)
		md5_compress(&message[off], hash);
	
	uint8_t block[BLOCK_LEN] = {0};
	size_t rem = len - off;
	if (rem > 0)
		memcpy(block, &message[off], rem);
	
	block[rem] = 0x80;
	rem++;
	if (BLOCK_LEN - rem < LENGTH_SIZE) {
		md5_compress(block, hash);
		memset(block, 0, sizeof(block));
	}
	
	block[BLOCK_LEN - LENGTH_SIZE] = (uint8_t)((len & 0x1FU) << 3);
	len >>= 5;
	for (int i = 1; i < LENGTH_SIZE; i++, len >>= 8)
		block[BLOCK_LEN - LENGTH_SIZE + i] = (uint8_t)(len & 0xFFU);
	md5_compress(block, hash);
}

void to_hex(char* dest, const uint8_t* values, size_t val_len) {
    for (int i = 0; i < val_len; i++)
    {
        sprintf((dest + 2*i),"%02X",*(values + i));
    }
}