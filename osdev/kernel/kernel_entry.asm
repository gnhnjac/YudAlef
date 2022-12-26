; Ensures that we jump straight into the kernel’s entry function.
bits 32
extern _entry
call _entry ; invoke main () in our C kernel
jmp $ ; Hang forever when we return from the kernel