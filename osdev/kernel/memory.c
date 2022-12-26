#include "memory.h"

/* Copy bytes from one place to another . */
void memcpy (char* dest , char* source , int no_bytes) {

	for (int i =0; i < no_bytes; i++) {
		*(dest + i) = *(source + i);
	}
}