#include "types.h"
#include "console.h"
#include "context.h"
#include "scheduler.h"

void timer_init(void) {
    // Read the timer frequency
    uint64_t cntfrq_el0;
    asm volatile("mrs %0, CNTFRQ_EL0" : "=r"(cntfrq_el0));

    // Set the timer interval to 1 second
    register uint64_t cntp_tval_el0 = cntfrq_el0;
    asm volatile("msr CNTP_TVAL_EL0, %0" :: "r"(cntp_tval_el0));

    // Enable the timer (bit 0 = enable)
    register uint64_t cntp_ctl_el0 = 1;
    asm volatile("msr CNTP_CTL_EL0, %0" :: "r"(cntp_ctl_el0));
}

static inline void timer_rearm(void) {
    unsigned long cntfrq;
    __asm__ volatile (
            "mrs %0, CNTFRQ_EL0\n"       // Read timer frequency
            : "=r"(cntfrq)
            );

    __asm__ volatile (
            "msr CNTP_TVAL_EL0, %0\n"    // Set timer interval
            :
            : "r"(cntfrq)
            );
}

context_t* timer_interrupt(context_t* interrupted_context) {
    console_out("Timer Interrupt: IRQ triggered! ");
    console_out("\n");

    context_t* next_context = scheduler_next(interrupted_context);

    timer_rearm();

    return next_context;
}
