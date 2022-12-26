#include "screen.h"
#include "strings.h"

void kmain();

void entry()
{

	kmain();

}


void kmain() {
	// Create a pointer to a char , and point it to the first text cell of video memory (i.e. the top - left of the screen )
	char *video_memory = (char *)0xb8000;
	clear_screen();

	for (int i = 0; i < 1000; i++)
	{	
		char args[sizeof(char) + sizeof(int)];
		args[0] = i%26;
		if (i % 3 == 0)
		{
			args[0] += 'A';

		}
		else
		{

			args[0] += 'a';

		}
		*((int *)((char *)args + 1)) = i;
		printf("Hello, world! character: %c, iteration: %d\n", (const void *)&args);
		for (int j = 0; j < 10000000; j++)
			continue;
	}
}