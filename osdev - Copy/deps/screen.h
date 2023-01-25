#include <stdint.h>

#define VIDEO_ADDRESS 0xb8000
#define MAX_ROWS 25
#define MAX_COLS 80

// Default color scheme
#define WHITE_ON_BLACK 0x0f

// Screen device I/O ports
#define REG_SCREEN_CTRL 0x3D4 // Internal register index
#define REG_SCREEN_DATA 0x3D5 // Internal register data
//refs
void print_char(const char character, int row, int col, char attribute_byte);
void blink_screen();
void unblink_screen();
int get_screen_offset(int row, int col);
int get_cursor();
void set_cursor(int offset);
void enable_cursor(uint8_t cursor_start, uint8_t cursor_end);
void disable_cursor();
void set_cursor_coords(int row, int col);
void putchar(char c);
void print_at(const char *msg, int row, int col, int attr_byte);
void print(const char *msg);
void print_color(const char *msg, int attr_byte);
int printf(const char *fmt, ...);
void clear_screen();
int handle_scrolling(int cursor_offset);
void display_logo();
void scroll_up();
void scroll_down();