; ===================================
; PRINTS OUT A STRING FROM MEMORY
; PARMAMS: MESSAGE OFFSET
; ===================================
print_str_mem:
	push bp
	mov bp, sp
	%define txt [bp+4]

	push ax
	push bx
	push si

	mov ah, 0x0e
	xor si, si

_printsm_loop:
	mov bx, txt
	mov al, byte[bx + si]
	cmp al, 0
	jz _printsm_end
	xor bx, bx
	int 0x10

	inc si

	jmp _printsm_loop
_printsm_end:

	pop si
	pop bx
	pop ax
	pop bp

	ret 2