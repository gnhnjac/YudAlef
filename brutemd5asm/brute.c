#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <time.h>

/* Function prototypes */

#define BLOCK_LEN 64  // In bytes
#define STATE_LEN 4  // In words

void md5_hash(const uint8_t message[], size_t len, uint32_t hash[static STATE_LEN]);

extern void md5_compress(const uint8_t block[static BLOCK_LEN], uint32_t state[static STATE_LEN]);

int cmpuint8_t(const uint8_t* v1, const uint8_t* v2, size_t len);

void to_hex(char* dest, const uint8_t* values, size_t val_len);

void little_to_big(uint32_t *array, int len);

int main(int argc, char **argv) {
    if (argc < 3)
        printf("Format must be: brute.c [MINRANGE] [MAXRANGE]");

    unsigned long minrange = (unsigned long)atoi(argv[1]);
    unsigned long maxrange = (unsigned long)atoi(argv[2]);
 
    char *desiredhash = "EC9C0F7EDCC18A98B1F31853B1813301";
    char *number = malloc(20 + 1);
    char *hex = malloc(32 + 1);

    for (unsigned long i = minrange; i < maxrange; i++)
    {
        sprintf(number, "%lu", i);
        size_t len = strlen(number);
        uint8_t *uint_msg = (uint8_t *)number;
        
        uint32_t hash[STATE_LEN];
		md5_hash(uint_msg, len, hash);
        little_to_big(hash, STATE_LEN);

        sprintf(hex, "%08X%08X%08X%08X", hash[0],hash[1],hash[2],hash[3]);

        if (strcmp(hex, desiredhash) == 0)
        {
                printf("%lu", i);
                free(hex);
                free(number);
                free(desiredhash);
                return 0;
        }
    }
    free(hex);
    free(number);
    free(desiredhash);
	return 1;
}

void little_to_big(uint32_t *array, int len)
{

    for (int i = 0; i < len; i++)
    {

        uint32_t num = *(array + i);
        uint32_t b0,b1,b2,b3;

        b0 = (num & 0x000000ff) << 24u;
        b1 = (num & 0x0000ff00) << 8u;
        b2 = (num & 0x00ff0000) >> 8u;
        b3 = (num & 0xff000000) >> 24u;

        *(array + i) = b0 | b1 | b2 | b3;


    }

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

uint8_t* hex_str_to_uint8(const char* string) {

    if (string == NULL)
        return NULL;

    size_t slength = strlen(string);
    if ((slength % 2) != 0) // must be even
        return NULL;

    size_t dlength = slength / 2;

    uint8_t* data = (uint8_t*)malloc(dlength);

    memset(data, 0, dlength);

    size_t index = 0;
    while (index < slength) {
        char c = string[index];
        int value = 0;
        if (c >= '0' && c <= '9')
            value = (c - '0');
        else if (c >= 'A' && c <= 'F')
            value = (10 + (c - 'A'));
        else if (c >= 'a' && c <= 'f')
            value = (10 + (c - 'a'));
        else
            return NULL;

        data[(index / 2)] += value << (((index + 1) % 2) * 4);

        index++;
    }

    return data;
}

int cmpuint8_t(const uint8_t* v1, const uint8_t* v2, size_t len)
{

    for (int i = 0; i < len; i++)
    {

        if ( *(v1 + i) != *(v2 + i) )
            return 1;

    }
    return 0;

}