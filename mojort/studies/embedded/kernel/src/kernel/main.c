#include "context.h"
#include "console.h"
#include "drivers/uart.h"
#include "drivers/gic.h"
#include "drivers/timer.h"
#include "scheduler.h"

extern void task1_entry(void);
extern void task2_entry(void);
extern addr_t EL0_TASK1_STACK_TOP;
extern addr_t EL0_TASK2_STACK_TOP;

context_t* kernel_main(void) {
    uart_init();
    console_out("-- Started ToyOS kernel --\n");

    gic_init();
    timer_init();
    unmask_irqs();

    const addr_t task1_stack_top = (addr_t)&EL0_TASK1_STACK_TOP;
    const addr_t task2_stack_top = (addr_t)&EL0_TASK2_STACK_TOP;

    context_init(get_task1_ctx(), task1_entry, task1_stack_top);
    context_init(get_task2_ctx(), task2_entry, task2_stack_top);

    console_out("-- Ended ToyOS kernel --\n");

    context_t* first_context = scheduler_first();
    return first_context;
}
