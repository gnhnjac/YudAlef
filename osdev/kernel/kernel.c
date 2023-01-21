#include "screen.h"
#include "idt.h"
#include "isrs.h"
#include "time.h"
#include <stdint.h>

void kmain();

void entry()
{

	kmain();

}

void kmain() {
	idt_install();
	disable_cursor();
	display_logo();
	for (;;);

	// for (int i = 0; i < 1000; i++)
	// {	

	// 	char lol = i%26;
	// 	if (i % 3 == 0)
	// 	{
	// 		lol += 'A';

	// 	}
	// 	else
	// 	{

	// 		lol += 'a';

	// 	}
	// 	int lolly = i;
	// 	printf("Hello, world! character: %c, iteration: 0x%x\n", lol, lolly);
	// 	for (int j = 0; j < 10000000; j++)
	// 		continue;
	// }

	return;
}
