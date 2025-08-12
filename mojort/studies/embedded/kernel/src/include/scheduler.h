#ifndef TOYOS_SCHEDULER_H
#define TOYOS_SCHEDULER_H

#include "context.h"

context_t* scheduler_first(void);
context_t* scheduler_next(context_t* current);
context_t* get_task1_ctx(void);
context_t* get_task2_ctx(void);

#endif /* TOYOS_SCHEDULER_H */
