org 0x7c00

jmp main

%include "utils/print/print_str_mem.asm"
%include "utils/hex/print_hex_word.asm"
%include "utils/disk/disk_load.asm"

data:
	msg db 'on god!',0xa, 0xd,0
	BOOT_DRIVE db 0

text:

	main:

		mov [BOOT_DRIVE], dl
		xor dh, dh
		mov bp, 0x8000
		mov sp, bp

		push 0
		push 0x9000
		push dx
		push 5
		call disk_load

		push word[0x9000]
		call print_hex_word

		push word[0x9000 + 512]
		call print_hex_word

		; push msg
		; call print_str_mem

		; push 0x1d0b
		; call print_hex_word

		jmp $


times 510-($-$$) db 0

dw 0xaa55

times 256 dw 0xdada
times 256 dw 0xface