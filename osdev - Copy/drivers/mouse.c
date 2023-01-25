#include "low_level.h"
#include "irq.h"
#include "screen.h"
#include "mouse.h"
#include <stdint.h>
#include <stdbool.h>

uint8_t PREVX = 40;
uint8_t PREVY = 12;
int8_t MOUSEX = 40;
int8_t MOUSEY = 12;
uint8_t interval = 0;
uint8_t color_attr = 3;
bool mouse_enabled = true;

placeholder mouset_buffer = {' ',0x0f};
placeholder mouseb_buffer = {' ',0x0f};
placeholder mouser_buffer = {' ',0x0f};

void mouse_wait(uint8_t type)
{
	uint32_t _timeout = 1000000;
	
	if (type == 0)
	{
		while (_timeout--)
		{
			if (inb(0x64) & 1) return;
			asm ("pause");
		}
	}
	else
	{
		while (_timeout--)
		{
			if (!(inb(0x64) & 2)) return;
			asm ("pause");
		}
	}

}

void disable_mouse()
{	
	char *video_memory = (char *)VIDEO_ADDRESS;
	mouse_enabled = false;
	print_char(mouset_buffer.ascii,MOUSEY,MOUSEX,mouset_buffer.attr);
		print_char(mouseb_buffer.ascii,MOUSEY+1,MOUSEX,mouseb_buffer.attr);
		print_char(mouser_buffer.ascii,MOUSEY,MOUSEX+1,mouser_buffer.attr);

}

void enable_mouse()
{
	mouse_enabled = true;
	print_char(' ',MOUSEY,MOUSEX,0x70);
	print_char(' ',MOUSEY+1,MOUSEX,0x70);
	print_char(' ',MOUSEY,MOUSEX+1,0x70);
}

void mouse_handler(struct regs *r)
{

	mouse_wait(0);
	uint8_t flags = inb(PS_DATA);
	mouse_wait(0);
	uint8_t xmov = inb(PS_DATA);
	mouse_wait(0);
	uint8_t ymov = inb(PS_DATA);
	mouse_wait(0);
	uint8_t zmov = inb(PS_DATA);

	if (!mouse_enabled)
		return;

	int left_click = flags & 1;
	int right_click = flags & 2;
	int middle_click = flags & 4;

	if (left_click)
		set_cursor_coords(MOUSEY, MOUSEX);
		color_attr += 1;
		color_attr = color_attr % 8;
	if (right_click)
	{
		int prev_cursor = get_cursor();
		print_char(' ',MOUSEY-1,MOUSEX-1,color_attr << 4);
		set_cursor(prev_cursor);
	}

	if (interval%5 == 0)
	{
		int8_t rel_x = xmov - ((flags << 4) & 0x100); // produce 2s complement only if the neg bit is set
		int8_t rel_y = ymov - ((flags << 3) & 0x100); // produce 2s complement only if the neg bit is set
		int8_t scroll = zmov & 0xF;

		// handle mouse mvmt

		MOUSEX += rel_x;

		if (MOUSEX < 0)
			MOUSEX = 0;
		else if (MOUSEX > 78)
			MOUSEX = 78;

		MOUSEY -= rel_y;

		if (MOUSEY < 0)
			MOUSEY = 0;
		else if (MOUSEY > 23)
			MOUSEY = 23;
		int prev_cursor = get_cursor();
		print_char(mouset_buffer.ascii,PREVY,PREVX,mouset_buffer.attr);
		print_char(mouseb_buffer.ascii,PREVY+1,PREVX,mouseb_buffer.attr);
		print_char(mouser_buffer.ascii,PREVY,PREVX+1,mouser_buffer.attr);

		PREVX = MOUSEX;
		PREVY = MOUSEY;

		char *video_memory = (char *)VIDEO_ADDRESS;

		mouset_buffer.ascii = *(video_memory + (MOUSEY*80 + MOUSEX)*2);
		mouset_buffer.attr = *(video_memory + (MOUSEY*80 + MOUSEX)*2 + 1);
		mouseb_buffer.ascii = *(video_memory + (MOUSEY*80 + MOUSEX + 80)*2);
		mouseb_buffer.attr = *(video_memory + (MOUSEY*80 + MOUSEX + 80)*2 + 1);
		mouser_buffer.ascii = *(video_memory + (MOUSEY*80 + MOUSEX + 1)*2);
		mouser_buffer.attr = *(video_memory + (MOUSEY*80 + MOUSEX + 1)*2 + 1);
		

		print_char(' ',MOUSEY,MOUSEX,0x70);
		print_char(' ',MOUSEY+1,MOUSEX,0x70);
		print_char(' ',MOUSEY,MOUSEX+1,0x70);
		set_cursor(prev_cursor);

		// handle scrolling

		if (scroll == VERTICAL_SCROLL_UP)
		{
			print("Scroll down\n");
			scroll_down();
		}
		else if (scroll == VERTICAL_SCROLL_DOWN)
			print("Scroll up\n");
			scroll_up();

	}
	interval++;

}


void ack()
{
	mouse_wait(0);
	uint8_t ack = inb(PS_DATA);                     // read back acknowledge. This should be 0xFA
}

void mouse_write(uint8_t byte)
{
	mouse_wait(1);
	outb(PS_CTRL, WRITE_TO_MOUSE); // tell the controller to address the mouse
	mouse_wait(1);
	outb(PS_DATA, byte); // default settings
	ack();

}

int identify()
{

	mouse_write(GET_MOUSE_ID); // get id
	mouse_wait(0);
	uint8_t id = inb(PS_DATA);
	return id;
}

void set_mouse_rate(int rate)
{

	mouse_write(MOUSE_CHANGE_SAMPLE);// change sample rate
	mouse_write(rate);
}

void mouse_install()
{


	__asm__ __volatile__ ("cli");

	mouse_wait(1);
	outb(PS_CTRL, 0xA8);

	mouse_wait(1);
	outb(PS_CTRL, 0x20); // read the configuration byte
	mouse_wait(0);
	char status_byte = inb(PS_DATA); // read ps status byte
	status_byte |= 2; // enable second ps2 port interrupt (irq12)
	status_byte &= 0b11011111;
	mouse_wait(1);
	outb(PS_CTRL, PS_DATA); // write to the configuration byte
	mouse_wait(1);
	outb(PS_DATA, status_byte);


	mouse_write(MOUSE_RESET); // reset
	mouse_wait(0);
	inb(PS_DATA);
	mouse_wait(0);
	inb(PS_DATA);


	mouse_write(MOUSE_DEFAULT);// default settings

	// activate scrolling

	set_mouse_rate(200);
	set_mouse_rate(100);
	set_mouse_rate(80);
	printf("MOUSE ID: %d\n",identify());

	mouse_write(MOUSE_PACKET);// activate data send

	__asm__ __volatile__ ("sti");

	irq_install_handler(12, mouse_handler);
}