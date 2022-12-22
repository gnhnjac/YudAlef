; ===================================
; LOAD SECTORS TO ES:BX FROM DRIVE
; PARMAMS: ES SEGMENT VALUE, BX OFFSET VALUE, DRIVE NUMBER, SECTORS TO BE READ
; ===================================
disk_load:
	
	push bp
	mov bp, sp
	%define es_val [bp+10]
	%define bx_off [bp+8]
	%define drive_num [bp+6]
	%define num_sectors [bp+4]

	pusha

	mov ax, es_val
	mov es, ax
	mov bx, bx_off

	mov ah , 0x02 ; BIOS read sector function
	mov al , num_sectors ; Read x sectors
	mov ch , 0x00 ; Select cylinder 0
	mov dh , 0x00 ; Select head 0
	mov dl, drive_num ; from drive x
	mov cl , 0x02 ; Start reading from second sector ( i.e. after the boot sector )
	int 0x13 ; BIOS interrupt

	jc _dl_disk_error ; Jump if error ( i.e. carry flag set )
	cmp num_sectors , al ; if AL ( sectors read ) != ( sectors expected )
	jne _dl_disk_error ; display error message

	popa

	pop bp

	ret 8

_dl_disk_error:
	push DISK_ERROR_MSG
	call print_str_mem
	jmp $

; Variables
DISK_ERROR_MSG db "Disk read error!" , 0
