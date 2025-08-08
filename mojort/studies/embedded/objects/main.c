// main.c
#include <stdio.h>
#include <stdint.h>

// Prototypes must match the Mojo exports (names and types)
int32_t add_ints(int32_t a, int32_t b);
double  saxpy_scalar(double a, double x, double y);
int32_t is_even(int32_t n);

int main(void) {
    printf("add_ints(2, 40) = %d\n", add_ints(2, 40));
    printf("saxpy_scalar(2.0, 3.0, 1.0) = %.1f\n", saxpy_scalar(2.0, 3.0, 1.0));
    printf("is_even(7) = %d\n", is_even(7));
    printf("is_even(8) = %d\n", is_even(8));
    return 0;
}
