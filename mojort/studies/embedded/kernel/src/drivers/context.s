.global save_context
save_context:
    // x0 contains lr
    // Save general-purpose registers into [sp], assuming it points to the context
    stp x1, x2,   [sp, #8 *  1]
    stp x3, x4,   [sp, #8 *  3]
    stp x5, x6,   [sp, #8 *  5]
    stp x7, x8,   [sp, #8 *  7]
    stp x9, x10,  [sp, #8 *  9]
    stp x11, x12, [sp, #8 * 11]
    stp x13, x14, [sp, #8 * 13]
    stp x15, x16, [sp, #8 * 15]
    stp x17, x18, [sp, #8 * 17]
    stp x19, x20, [sp, #8 * 19]
    stp x21, x22, [sp, #8 * 21]
    stp x23, x24, [sp, #8 * 23]
    stp x25, x26, [sp, #8 * 25]
    stp x27, x28, [sp, #8 * 27]
    stp x29, x30, [sp, #8 * 29]     // FP and LR (wrong LR from EL1!)
    str x0, [sp, #8 * 30]           // save real LR from EL0 (moved to x0 by caller)

    // Save sp_el0, or just the current sp (optional TODO for nested IRQs)
    mrs x0, SP_EL0
    str x0, [sp, #8 * 31]       // ctx->sp = sp

    // Save return address -- interrupted PC
    mrs x1, ELR_EL1
    str x1, [sp, #8 * 32]       // ctx->elr_el1 = interrupted pc

    // Save exception state
    mrs x2, SPSR_EL1
    str x2, [sp, #8 * 33]       // ctx->spsr_el1 = processor status

    // Get context pointer from sp to x0
    mov x0, sp

    // Reset the kernel stack
    ldr x3, =EL1_KERNEL_STACK_TOP
    mov sp, x3

    ret

.global restore_context
restore_context:
    // Assumes sp already points to the context
    ldr x1, [sp, #8 * 31]
    msr SP_EL0, x1              // Set the user mode stack pointer

    ldr x1, [sp, #8 * 32]
    msr ELR_EL1, x1             // Set return address

    ldr x1, [sp, #8 * 33]
    msr SPSR_EL1, x1            // Restore status register

    ldp x0, x1, [sp, #8 *  0]
    ldp x2, x3, [sp, #8 *  2]
    ldp x4, x5, [sp, #8 *  4]
    ldp x6, x7, [sp, #8 *  6]
    ldp x8, x9, [sp, #8 *  8]
    ldp x10, x11, [sp, #8 * 10]
    ldp x12, x13, [sp, #8 * 12]
    ldp x14, x15, [sp, #8 * 14]
    ldp x16, x17, [sp, #8 * 16]
    ldp x18, x19, [sp, #8 * 18]
    ldp x20, x21, [sp, #8 * 20]
    ldp x22, x23, [sp, #8 * 22]
    ldp x24, x25, [sp, #8 * 24]
    ldp x26, x27, [sp, #8 * 26]
    ldp x28, x29, [sp, #8 * 28]
    ldr x30,       [sp, #8 * 30]

    eret                        // Return to EL0 using the state we just loaded
