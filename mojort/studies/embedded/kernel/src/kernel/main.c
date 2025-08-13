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

uint32_t mmio_read32(uint64_t addr) {
    return *(volatile uint32_t *)addr;
}
void mmio_write32(uint64_t addr, uint32_t v) {
    *(volatile uint32_t *)addr = v;
}

//int sum(int a, int b) {
//    return a + b;
//}
int sum(int a, int b);

void print_operation(void) {
    const int answer = sum(39, 3);
    if (42 == answer) {
        console_out("-- The result of 39 + 3 is 42!\n");
    } else {
        console_out("-- The result is WRONG!\n");
    }
}

context_t* kernel_main(void) {
    uart_init();
    console_out("-- Started ToyOS kernel --\n");
    print_operation();

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
