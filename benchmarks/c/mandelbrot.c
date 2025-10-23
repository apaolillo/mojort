// mandelbrot.c
// Transpiled from: https://github.com/dario-marvin/Mandelbrot/blob/master/Mandelbrot.cc
#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif /* _GNU_SOURCE */

#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <math.h>
#include <time.h>
#include <stdint.h>

static int mandelbrotComplex(double complex c) {
    const int limit = 1000;
    double complex z = c;

    for (int i = 0; i < limit; ++i) {
        if (cabs(z) > 2.0) return i;
        z = z * z + c;
    }
    return limit;
}

static int mandelbrotSplit(double real, double imag) {
    const int limit = 1000;
    double zReal = real;
    double zImag = imag;

    for (int i = 0; i < limit; ++i) {
        double r2 = zReal * zReal;
        double i2 = zImag * zImag;

        if (r2 + i2 > 4.0) return i;

        zImag = 2.0 * zReal * zImag + imag;
        zReal = r2 - i2 + real;
    }
    return limit;
}

static inline int64_t now_us(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (int64_t)ts.tv_sec * 1000000LL + ts.tv_nsec / 1000LL;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "usage: %s <width>\n", argv[0]);
        return 1;
    }

    int width = atoi(argv[1]);
    int heigth = width; // keep original variable name from C++ code

    double x_start = -2.0;
    double x_fin   =  0.47;
    double y_start = -1.12;
    double y_fin   =  1.12;

    double dx = (x_fin - x_start) / (width  - 1);
    double dy = (y_fin - y_start) / (heigth - 1);

    int64_t t1 = now_us();
    long long a = 0;

    for (int i = 0; i < heigth; i++) {
        for (int j = 0; j < width; j++) {
            double x = x_start + j * dx;   // current real value
            double y = y_fin   - i * dy;   // current imaginary value

            // a += mandelbrotSplit(x, y);
            a += mandelbrotComplex(x + y * I);
        }
    }

    int64_t t2 = now_us();

    // printing "a" the sum of all element in the mandelbrot matrix
    // done so the compiler wont remove the workload
    printf("checkvalue: %lld\n", a);
    printf("runtime: %lld µs\n", (long long)(t2 - t1));

    return 0;
}
