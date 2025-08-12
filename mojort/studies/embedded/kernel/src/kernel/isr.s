.global el1_sync_handler
el1_sync_handler:
    b .

.global el1_svc_handler
el1_svc_handler:
    b .

.global irq_handler
irq_handler:
    str x0, [sp, #8 * 0]
    mov x0, x30                 // get LR (link register) = return address
    bl save_context

    bl timer_interrupt

    // x0 now contains pointer to the first context to run
    mov sp, x0
    b restore_context
