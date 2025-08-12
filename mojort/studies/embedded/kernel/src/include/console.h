#ifndef TOYOS_CONSOLE_H
#define TOYOS_CONSOLE_H

#include "drivers/uart.h"

static void console_out(const char* s) {
    uart_send_string(s);
}

#endif /* TOYOS_CONSOLE_H */
