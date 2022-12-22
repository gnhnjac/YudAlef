; ===================================
; PRINTS OUT A HEX WORD TO THE SCREEN
; PARMAMS: WORD NUMBER
; ===================================
print_hex_word:

	push bp
	mov bp, sp
	%define num [bp+4]

	push ax
	push bx
	push si

	mov ax, num
	mov si, 3

_phw_loop:

	mov bx, ax
	and bx, 0xF

	push ax
	mov al, [HEX_TABLE+bx]
	mov bx, HEX_OUT
	mov [bx+si+2], al
	pop ax

	dec si
	shr ax, 4

	cmp ax, 0
	jnz _phw_loop

	push HEX_OUT
	call print_str_mem

	pop si
	pop bx
	pop ax
	pop bp

	ret 2

; Variables
HEX_OUT db '0x0000',0xa, 0xd,0
HEX_TABLE db '0123456789abcdef'