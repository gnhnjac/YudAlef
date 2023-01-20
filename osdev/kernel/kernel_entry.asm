; Ensures that we jump straight into the kernel’s entry function.
; Also contains external functions that have to be written in assembly.
bits 32
extern _entry
call _entry ; invoke main () in our C kernel
jmp $ ; Hang forever when we return from the kernel

; EXCEPTION IDT GATES
global _isr0
global _isr1
global _isr2
global _isr3
global _isr4
global _isr5
global _isr6
global _isr7
global _isr8
global _isr9
global _isr10
global _isr11
global _isr12
global _isr13
global _isr14
global _isr15
global _isr16
global _isr17
global _isr18
global _isr19
global _isr20
global _isr21
global _isr22
global _isr23
global _isr24
global _isr25
global _isr26
global _isr27
global _isr28
global _isr29
global _isr30
global _isr31
; CUSTOM IDT GATES
; TODO

;  0: Divide By Zero Exception
_isr0:
    cli ; clear interrupts to prevent irqs from executing until we handle the exception.
    push byte 0    ; A normal ISR stub that pops a dummy error code to keep a
                   ; uniform stack frame
    push byte 0
    jmp isr_common_stub

;  1: Debug Exception
_isr1:
    cli
    push byte 0
    push byte 1
    jmp isr_common_stub
    
;  2: Non Maskable Interrupt Exception
_isr2:
   cli
   push byte 0
   push byte 2
   jmp isr_common_stub

; Breakpoint Exception
_isr3:
   cli
   push byte 0
   push byte 3
   jmp isr_common_stub

; Into Detected Overflow Exception
_isr4:
   cli
   push byte 0
   push byte 4
   jmp isr_common_stub

; Out of Bounds Exception
_isr5:
   cli
   push byte 0
   push byte 5
   jmp isr_common_stub

; Invalid Opcode Exception
_isr6:
   cli
   push byte 0
   push byte 6
   jmp isr_common_stub

; No Coprocessor Exception
_isr7:
   cli
   push byte 0
   push byte 7
   jmp isr_common_stub

;  8: Double Fault Exception (With Error Code!)
_isr8:
    cli
    push byte 8        ; This one already pushes an error code onto the stack so we only push the sequential number of the gate.
    jmp isr_common_stub

;  9: Coprocessor Segment Overrun Exception
_isr9:
   cli
   push byte 0
   push byte 9
   jmp isr_common_stub
; Bad TSS Exception
_isr10:
   cli
   push byte 10
   jmp isr_common_stub
; Segment Not Present Exception
_isr11:
   cli
   push byte 11
   jmp isr_common_stub
;  Stack Fault Exception
_isr12:
   cli
   push byte 12
   jmp isr_common_stub
;  General Protection Fault Exception
_isr13:
   cli
   push byte 13
   jmp isr_common_stub
;  Page Fault Exception
_isr14:
   cli
   push byte 14
   jmp isr_common_stub
;  Unknown Interrupt Exception
_isr15:
   cli
   push byte 0
   push byte 15
   jmp isr_common_stub
;  Coprocessor Fault Exception
_isr16:
   cli
   push byte 0
   push byte 16
   jmp isr_common_stub
;  Alignment Check Exception (486+)
_isr17:
   cli
   push byte 17
   jmp isr_common_stub
;  Machine Check Exception (Pentium/586+)
_isr18:
   cli
   push byte 0
   push byte 18
   jmp isr_common_stub
;  19-31: Reserved Exceptions
_isr19:
        cli
        push byte 0
        push byte 19
        jmp isr_common_stub

_isr20:
        cli
        push byte 0
        push byte 20
        jmp isr_common_stub

_isr21:
        cli
        push byte 0
        push byte 21
        jmp isr_common_stub

_isr22:
        cli
        push byte 0
        push byte 22
        jmp isr_common_stub

_isr23:
        cli
        push byte 0
        push byte 23
        jmp isr_common_stub

_isr24:
        cli
        push byte 0
        push byte 24
        jmp isr_common_stub

_isr25:
        cli
        push byte 0
        push byte 25
        jmp isr_common_stub

_isr26:
        cli
        push byte 0
        push byte 26
        jmp isr_common_stub

_isr27:
        cli
        push byte 0
        push byte 27
        jmp isr_common_stub

_isr28:
        cli
        push byte 0
        push byte 28
        jmp isr_common_stub

_isr29:
        cli
        push byte 0
        push byte 29
        jmp isr_common_stub

_isr30:
        cli
        push byte 30
        jmp isr_common_stub

_isr31:
        cli
        push byte 0
        push byte 31
        jmp isr_common_stub

; We call a C function in here. We need to let the assembler know
; that '_fault_handler' exists in another file
extern _fault_handler

; This is our common ISR stub. It saves the processor state, sets
; up for kernel mode segments, calls the C-level fault handler,
; and finally restores the stack frame.
isr_common_stub:
    pusha
    push ds
    push es
    push fs
    push gs
    mov ax, 0x10   ; Load the Kernel Data Segment descriptor (16 bytes after start of GDT so 0x10)
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov eax, esp   ; Push us the stack
    push eax
    mov eax, _fault_handler
    call eax       ; A special call, preserves the 'eip' register
    pop eax
    pop gs
    pop fs
    pop es
    pop ds
    popa
    add esp, 8     ; Cleans up the pushed error code and pushed ISR number ()
    iret           ; pops 5 things at once: CS, EIP, EFLAGS, SS, and ESP