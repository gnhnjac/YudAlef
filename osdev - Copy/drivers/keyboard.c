#include "irq.h"
#include "keyboard.h"
#include "low_level.h"
#include "screen.h"

// status byte for keyboard
// [n,n,n,n,caps,shift,alt,ctrl]
unsigned char kstatus = 0;

void enable_shift()
{

  kstatus |= 0b00000100;

}

void disable_shift()
{

  kstatus &= ~0b00000100;

}

int check_shift()
{

  return kstatus & 0b00000100;

}

void enable_ctrl()
{

  kstatus |= 0b00000001;

}

void disable_ctrl()
{

  kstatus &= ~0b00000001;

}

int check_ctrl()
{

  return kstatus & 0b00000001;

}

void enable_caps()
{

  kstatus |= 0b00001000;

}

void disable_caps()
{

  kstatus &= ~0b00001000;

}

int check_caps()
{

  return kstatus & 0b00001000;

}

void enable_alt()
{

  kstatus |= 0b00000010;

}

void disable_alt()
{

  kstatus &= ~0b00000010;

}

int check_alt()
{

  return kstatus & 0b00000010;

}

// us keyboard layout scancode->ascii
unsigned char kbdus[128] =
{
    0,  27, '1', '2', '3', '4', '5', '6', '7', '8',	/* 9 */
  '9', '0', '-', '=', '\b',	/* Backspace */
  '\t',			/* Tab */
  'q', 'w', 'e', 'r',	/* 19 */
  't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\n',	/* Enter key */
    0,			/* 29   - Control */
  'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';',	/* 39 */
 '\'', '`',   0,		/* Left shift */
 '\\', 'z', 'x', 'c', 'v', 'b', 'n',			/* 49 */
  'm', ',', '.', '/',   0,				/* Right shift */
  '*',
    0,	/* Alt */
  ' ',	/* Space bar */
    0,	/* Caps lock */
    0,	/* 59 - F1 key ... > */
    0,   0,   0,   0,   0,   0,   0,   0,
    0,	/* < ... F10 */
    0,	/* 69 - Num lock*/
    0,	/* Scroll Lock */
    0,	/* Home key */
    0,	/* Up Arrow */
    0,	/* Page Up */
  '-',
    0,	/* Left Arrow */
    0,
    0,	/* Right Arrow */
  '+',
    0,	/* 79 - End key*/
    0,	/* Down Arrow */
    0,	/* Page Down */
    0,	/* Insert Key */
    0,	/* Delete Key */
    0,   0,   0,
    0,	/* F11 Key */
    0,	/* F12 Key */
    0,	/* All other keys are undefined */
};

unsigned char kbdus_shift[128] =
{
    0,  27, '!', '@', '#', '$', '%', '^', '&', '*', /* 9 */
  '(', ')', '_', '+', '\b', /* Backspace */
  '\t',     /* Tab */
  'Q', 'W', 'E', 'R', /* 19 */
  'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '\n', /* Enter key */
    0,      /* 29   - Control */
  'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', /* 39 */
 '\"', '~',   0,    /* Left shift */
 '|', 'Z', 'X', 'C', 'V', 'B', 'N',      /* 49 */
  'M', '<', '>', '?',   0,        /* Right shift */
  '*',
    0,  /* Alt */
  ' ',  /* Space bar */
    0,  /* Caps lock */
    0,  /* 59 - F1 key ... > */
    0,   0,   0,   0,   0,   0,   0,   0,
    0,  /* < ... F10 */
    0,  /* 69 - Num lock*/
    0,  /* Scroll Lock */
    0,  /* Home key */
    0,  /* Up Arrow */
    0,  /* Page Up */
  '-',
    0,  /* Left Arrow */
    0,
    0,  /* Right Arrow */
  '+',
    0,  /* 79 - End key*/
    0,  /* Down Arrow */
    0,  /* Page Down */
    0,  /* Insert Key */
    0,  /* Delete Key */
    0,   0,   0,
    0,  /* F11 Key */
    0,  /* F12 Key */
    0,  /* All other keys are undefined */
};

/* Handles the keyboard interrupt */
void keyboard_handler(struct regs *r)
{
    outb(0x20, 0x20);
    unsigned char scancode;

    /* Read from the keyboard's data buffer */
    scancode = inb(0x60);

    /* If the top bit of the byte we read from the keyboard is
    *  set, that means that a key has just been released */
    if (scancode & 0x80)
    {
        /* You can use this one to see if the user released the
        *  shift, alt, or control keys... */

      if (scancode == 170 || scancode == 182) // shift
      {

        disable_shift();

      }
      else if (scancode == 157) // ctrl
      {

        disable_ctrl();

      }
      else if (scancode == 184) // alt
      {

        disable_alt();

      }
      else if (scancode == 186) // caps
      {

        if(check_caps())
          disable_caps();
        else
          enable_caps();

      }

    }
    else
    {
        if (scancode == 42 || scancode == 54) // shift
        {

          enable_shift();
          return;

        }
        else if (scancode == 29) // ctrl
        {

          enable_ctrl();
          return;

        }
        else if (scancode == 56) // alt
        {

          enable_alt();
          return;

        }
        else if (scancode == 58) // caps
        {
          return;
        }

        /* Here, a key was just pressed. Please note that if you
        *  hold a key down, you will get repeated key press
        *  interrupts. */

        /* Just to show you how this works, we simply translate
        *  the keyboard scancode into an ASCII value, and then
        *  display it to the screen. You can get creative and
        *  use some flags to see if a shift is pressed and use a
        *  different layout, or you can add another 128 entries
        *  to the above layout to correspond to 'shift' being
        *  held. If shift is held using the larger lookup table,
        *  you would add 128 to the scancode when you look for it */
        if (check_shift())
        {
          putchar(kbdus_shift[scancode]);
        }
        else
        {

          char ascii = kbdus[scancode];
          if (check_caps() && 'a' <= ascii && 'z' >= ascii)
            ascii -= 'a'-'A';

          putchar(ascii);
        }
    }
}

void keyboard_install()
{

    irq_install_handler(1, keyboard_handler);

}