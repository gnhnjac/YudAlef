#include "memory.h"

/* Copy bytes from one place to another . */
void memcpy (unsigned char* dest , const char* source , int count) {

	for (int i =0; i < count; i++) {
		*(dest + i) = *(source + i);
	}
}

unsigned char *memset(unsigned char *dest, unsigned char val, int count)
{
    /* set 'count' bytes in 'dest' to 'val'. */

    for (int i = 0; i < count; i++)
    {

    	*(dest + i) = val;

    }
}

unsigned short *memsetw(unsigned short *dest, unsigned short val, int count)
{
   for (int i = 0; i < count; i++)
    {

    	*(dest + i) = val;

    }
}