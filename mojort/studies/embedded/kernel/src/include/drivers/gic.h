#ifndef TOYOS_GIC_H
#define TOYOS_GIC_H

void gic_init(void);

static inline void unmask_irqs(void) {
    asm volatile("msr DAIFClr, #2" ::: "memory");
}

#endif /* TOYOS_GIC_H */
