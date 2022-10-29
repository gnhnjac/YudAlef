#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <md5.c>

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

int main(int argc, char **argv) {
    if (argc < 3)
        printf("Format must be: brute.c [MINRANGE] [MAXRANGE]");

    unsigned long minrange = (unsigned long)atoi(argv[1]);
    unsigned long maxrange = (unsigned long)atoi(argv[2]);
 
    uint8_t *desiredhash = hex_str_to_uint8("EC9C0F7EDCC18A98B1F31853B1813301");
    char *number = malloc(12 + 1);
	MD5Context ctx;
    for (unsigned long i = minrange; i < maxrange; i++)
    {
        sprintf(number, "%lu", i);
        //uint8_t *output = md5String(number);
		md5Init(&ctx);
		md5Update(&ctx, (uint8_t *)number, strlen(number));
		md5Finalize(&ctx);
        if (cmpuint8_t(ctx.digest, desiredhash, 16) == 0)
        {
                printf("%s", number);
                // free(output);
                free(number);
                free(desiredhash);
                return 0;
        }
        // free(output);
    }
    free(number);
    free(desiredhash);
	return 1;
}