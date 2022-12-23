org 0x7c00
bits 16
BEGIN_RM:
	mov bp, 0x9000 ; init the stack
	mov sp, bp

	push rm_msg
	call print_str_mem

	; switch to 32 bit protected mode
	call switch_to_pm


bits 32
BEGIN_PM:

	push pm_msg
	call print_str_mem32
	jmp $

; 16 bit rm files
%include "print_str_mem.asm"
%include "print_hex_word.asm"
%include "gdt.asm"

; 32 bit pm files
%include "print_str_mem32.asm"
%include "switch_to_pm.asm"

; Global variables
	rm_msg db '16-bit Real Mode running...',0xa, 0xd,0
	pm_msg db 'Successfully switched to 32-bit protected mode!', 0

times 510-($-$$) db 0

dw 0xaa55