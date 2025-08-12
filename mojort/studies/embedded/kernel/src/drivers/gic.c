#include "drivers/gic.h"

#include "types.h"

#define GICD_CTLR      0x08000000UL   // GIC Distributor Control Register
#define GICD_ISENABLER 0x08000100UL   // GIC Distributor Set-Enable Registers base
#define GICC_CTLR      0x08010000UL   // GIC CPU Interface Control Register
#define GICC_PMR       0x08010004UL   // GIC Interrupt Priority Mask Register

void gic_init(void) {
    // Enable GIC Distributor
    volatile uint32_t *gicd_ctlr = (uint32_t *)GICD_CTLR;
    *gicd_ctlr = 1;

    // Enable GIC CPU Interface
    volatile uint32_t *gicc_ctlr = (uint32_t *)GICC_CTLR;
    *gicc_ctlr = 1;

    // Set Priority Mask Register (allow all priorities)
    volatile uint32_t *gicc_pmr = (uint32_t *)GICC_PMR;
    *gicc_pmr = 0xFF;

    // Enable timer interrupt (ID 30)
    uint32_t irq_id = 30;
    uint32_t reg_index = irq_id / 32;
    uint32_t bit_offset = irq_id % 32;
    uint32_t mask = 1u << bit_offset;

    volatile uint32_t *gicd_isenabler = (uint32_t *)(GICD_ISENABLER + (reg_index * 4));
    *gicd_isenabler = mask;
}
