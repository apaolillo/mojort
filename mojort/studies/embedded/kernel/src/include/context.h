#ifndef TOYOS_CONTEXT_H
#define TOYOS_CONTEXT_H

#include "types.h"

typedef struct context {
    uint64_t regs[31];     // x0 - x30
    uint64_t sp;           // SP_EL0 (or SP during exception)
    uint64_t elr_el1;      // Return address
    uint64_t spsr_el1;     // Processor state
} context_t;

static void context_init(context_t *ctx, void (*entry_point)(void), uint64_t stack_top) {
    for (int i = 0; i < 31; ++i) {
        ctx->regs[i] = 0xDEADBEEF00000000UL + i;  // Canary pattern
    }

    ctx->sp = stack_top;
    ctx->elr_el1 = (uint64_t)entry_point;
    ctx->spsr_el1 = 0x00000000;  // Default: unmasked, EL0, AArch64
}

#endif /* TOYOS_CONTEXT_H */
