#include "screen.h"
#include "idt.h"
#include "irq.h"
#include "timer.h"
#include "keyboard.h"
#include "mouse.h"

void kmain();

void entry()
{

	kmain();

}

void kmain() {
	idt_install();
	irq_install();
	timer_install();
	display_logo();
	clear_screen();
	keyboard_install();
	mouse_install();

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
	// 	sleep(100);

	// }

	return;
}
