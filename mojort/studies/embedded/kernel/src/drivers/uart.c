#include "types.h"

#define UART_BASE 0x09000000
#define UART_DR   (*(volatile uint32_t *)(UART_BASE + 0x00)) // Data register
#define UART_FR   (*(volatile uint32_t *)(UART_BASE + 0x18)) // Flag register

#define UART_FR_TXFF (1 << 5) // Transmit FIFO Full
#define UART_FR_RXFE (1 << 4) // Receive FIFO Empty

// Initialize the UART (optional for QEMU's PL011, as it's ready by default)
void uart_init(void) {
    // UART initialization is optional in QEMU
}

// Send a character
void uart_send(char c) {
    while (UART_FR & UART_FR_TXFF) {
        // Wait until the Transmit FIFO is not full
    }
    UART_DR = c;
}

// Receive a character
char uart_receive(void) {
    while (UART_FR & UART_FR_RXFE) {
        // Wait until the Receive FIFO is not empty
    }
    return (char)UART_DR;
}

// Send a string
void uart_send_string(const char *str) {
    while (*str) {
        uart_send(*str++);
    }
}

// Send a character
void uart_send_char(char c) {
    uart_send(c);
}
