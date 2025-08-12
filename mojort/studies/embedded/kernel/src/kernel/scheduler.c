#include "scheduler.h"

// Declare two static contexts for the tasks
static context_t task1_ctx;
static context_t task2_ctx;

static context_t* current_ctx = 0;

context_t* scheduler_first(void) {
    current_ctx = &task1_ctx;
    return current_ctx;
}

context_t* scheduler_next(context_t* current) {
    if (current == &task1_ctx) {
        current_ctx = &task2_ctx;
    } else {
        current_ctx = &task1_ctx;
    }
    return current_ctx;
}

// Expose access to the static task contexts (for init)
context_t* get_task1_ctx(void) { return &task1_ctx; }
context_t* get_task2_ctx(void) { return &task2_ctx; }
