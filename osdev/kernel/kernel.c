#include "screen.h"

void start () {
	// Create a pointer to a char , and point it to the first text cell of video memory (i.e. the top - left of the screen )
	char *video_memory = (char *)0xb8000;
	// At the address pointed to by video_memory , store the character ’X’
	char *abc = "z";
	*video_memory = *(abc);
	*(video_memory + 2) = 'Y';
	print("HEY!");
	//clear_screen();

	//char *msg = "hey!";

	//print(msg);
	//print_at(msg, -1, -1);
}