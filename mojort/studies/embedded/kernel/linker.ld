ENTRY(_start)

SECTIONS
{
    . = 0x40000000;
    .vector : { *(.vector) } /* put the vector table first */
    . = ALIGN(0x1000);
    .text : { *(.text) }
    .data : { *(.data) }
    .bss : { *(.bss COMMON) }
    . = ALIGN(0x1000);

    . = . + 0x1000; /* 4 KB for EL1 stack */
    EL1_KERNEL_STACK_TOP = .;

    . = . + 0x1000; /* 4 KB for EL0 stack */
    EL0_TASK1_STACK_TOP = .;

    . = . + 0x1000; /* 4 KB for EL0 stack */
    EL0_TASK2_STACK_TOP = .;
}
