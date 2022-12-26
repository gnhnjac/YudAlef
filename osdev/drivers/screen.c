#include "screen.h"
#include "low_level.h"
#include "memory.h"
#include "std.h"
#include "strings.h"

/* Print a char on the screen at col, row, or at cursor position */
void print_char(const char character, int row, int col, char attribute_byte) 
{
	/* Create a byte ( char ) pointer to the start of video memory */
	char *vidmem = (char *)VIDEO_ADDRESS;
	/* If attribute byte is zero , assume the default style . */
	if (!attribute_byte) {
		attribute_byte = WHITE_ON_BLACK;
	}
	/* Get the video memory offset for the screen location */
	int offset;
	/* If col and row are non-negative, use them for offset. */
	if ( col >= 0 && row >= 0) {
		offset = get_screen_offset(row, col);
		/* Otherwise, use the current cursor position. */
	} else {
		offset = get_cursor();
	}
	// If we see a newline character, set offset to the end of
	// current row, so it will be advanced to the first col
	// of the next row.
	if (character == '\n') {

		int current_row = offset / (2 * MAX_COLS);
		offset = get_screen_offset(current_row, MAX_COLS-1);
	// Otherwise , write the character and its attribute byte to
	// video memory at our calculated offset .
	} else {
		vidmem [offset] = character;
		vidmem [offset + 1] = attribute_byte;
	}
	// Update the offset to the next character cell , which is
	// two bytes ahead of the current cell .
	offset += 2;
	// Make scrolling adjustment, for when we reach the bottom
	// of the screen.
	offset = handle_scrolling(offset);
	// Update the cursor position on the screen device.
	set_cursor(offset);
}

int get_screen_offset(int row, int col) 
{

	return 2*(row * MAX_COLS + col);

}

int get_cursor() 
{
	// The device uses its control register as an index
	// to select its internal registers , of which we are
	// interested in:
	// reg 14: which is the high byte of the cursor’s offset
	// reg 15: which is the low byte of the cursor’s offset
	// Once the internal register has been selected , we may read or
	// write a byte on the data register .
	port_byte_out(REG_SCREEN_CTRL, 14);
	int offset = port_byte_in(REG_SCREEN_DATA) << 8;
	port_byte_out(REG_SCREEN_CTRL, 15);
	offset += port_byte_in(REG_SCREEN_DATA);
	// Since the cursor offset reported by the VGA hardware is the
	// number of characters, we multiply by two to convert it to
	// a character cell offset.
	return offset*2;
}

void set_cursor(int offset) 
{
	offset /= 2; // Convert from cell offset to char offset.
	// This is similar to get_cursor, only now we write
	// bytes to those internal device registers.
	port_byte_out(REG_SCREEN_CTRL, 14);
	port_byte_out(REG_SCREEN_DATA, (unsigned char)(offset >> 8));
	port_byte_out(REG_SCREEN_CTRL, 15);
	port_byte_out(REG_SCREEN_DATA, (unsigned char)(offset));
}

void putchar(char c)
{

	print_char(c, -1, -1, WHITE_ON_BLACK);

}

void print_at(const char *msg, int row, int col) 
{
	// maybe redundant
	if ( col >= 0 && row >= 0) {
		set_cursor(get_screen_offset(row, col));
	}
	while (*msg)
	{

		print_char(*msg++, row, col, WHITE_ON_BLACK);
	}
}

void print(const char *msg) 
{

	print_at(msg, -1, -1);

}

int printf(const char *fmt, const void *args)
{

	const char *orig = fmt;

	while (*fmt)
	{

		if (*fmt == '%' && ((*(fmt-1) != '\\' && fmt != orig) || fmt == orig))
		{

			fmt++;

			if (*fmt == 'd')
			{

				char buff[30];
				int_to_dec(*((int *)args), buff);
				print(buff);
				(int *)args++;

			}
			else if(*fmt == 'c')
			{
				putchar(*((char *)args));
				(char *)args++;

			}
			else
			{
				printf("Unknown format type \\%%c", fmt);
				return STDERR;

			}

		}
		else if(*fmt == '\\')
		{	
			fmt++;
			continue;
		}
		else
		{

			putchar(*fmt);

		}

		fmt++;

	}

	return STDOK;

}

void clear_screen() 
{

	char *video_memory = (char *)VIDEO_ADDRESS;

	for(int i = 0; i < MAX_COLS*MAX_ROWS*2; i += 2)
	{
		*(video_memory + i) = ' ';
		//*(video_memory + 1) = 0x0f;
	}
	//Move the cursor back to the top left .
	set_cursor(get_screen_offset(0, 0));
}

int handle_scrolling(int cursor_offset)
{

	if (cursor_offset < MAX_ROWS*MAX_COLS*2)
	{
		return cursor_offset;
	}

	for (int i = 1; i < MAX_ROWS; i++)
	{

		memcpy((char *)(VIDEO_ADDRESS + get_screen_offset(i-1, 0)), (char *)(VIDEO_ADDRESS + get_screen_offset(i, 0)),2*MAX_COLS);

	}

	char *last_line = (char *)(VIDEO_ADDRESS + get_screen_offset(MAX_ROWS-1, 0));

	for (int i = 0; i < MAX_COLS*2; i++)
	{

		*(last_line + i) = 0;

	}

	cursor_offset -= 2*MAX_COLS;

	return cursor_offset;

}