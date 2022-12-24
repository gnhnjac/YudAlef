# Default make target .
all: os-image

# Run bochs to simulate booting of our code.
run: all
	bochs

# This is the actual disk image that the computer loads,
# which is the combination of our compiled bootsector and kernel
os-image: boot_sect.bin kernel.bin
	copy /b boot_sect.bin+kernel.bin os-image

# This builds the binary of our kernel from two object files :
# - the kernel_entry , which jumps to start() in our kernel
# - the compiled C kernel
# $^ is substituted with all of the target's dependency files
kernel.bin: kernel_entry.o kernel.o
	ld -T NUL -o kernel.tmp -Ttext 0x1000 $^
	objcopy -O binary -j .text kernel.tmp kernel.bin
	del /f kernel.tmp

# Build our kernel object file.
#$< is the first dependancy and $@ is the target file
kernel.o: kernel.c
	gcc -ffreestanding -c $< -o $@

# Build our kernel entry object file.
#$< is the first dependancy and $@ is the target file
kernel_entry.o: kernel_entry.asm
	nasm $< -f elf -o $@

# Assemble the boot sector to raw machine code
# The -I options tells nasm where to find our useful assembly
# routines that we include in boot_sect.asm
boot_sect.bin : boot_sect.asm
	nasm -f bin @< -I 'routines/' -o $@

clean:
	del /f *.bin 
	del /f *.o
	del os-image

# Disassemble our kernel - might be useful for debugging .
kernel.dis: kernel.bin
	ndisasm -b 32 $< > $@