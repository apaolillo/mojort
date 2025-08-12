.global _start

.section .text
_start:
    ldr x0, =_vectors               // Load the address of the vector table
    msr VBAR_EL1, x0                // Set the vector base address
    isb                             // Ensure the change takes effect
    ldr x1, =EL1_KERNEL_STACK_TOP   // Set up kernel stack pointer
    mov sp, x1

    bl kernel_main

    // x0 now contains pointer to the first context to run
    mov sp, x0
    b restore_context

_end:
    b .
