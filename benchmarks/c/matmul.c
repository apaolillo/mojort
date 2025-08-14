// matrix_mul_weird.c
// C translation of the provided C++ code.

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include <assert.h>

typedef struct {
    int w, h;
    int *data;  // length = w * h
} Matrix;

static inline int64_t now_us(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (int64_t)ts.tv_sec * 1000000LL + ts.tv_nsec / 1000LL;
}

static Matrix matrix_new(int w, int h,int initempty) {
    Matrix m;
    m.w = w;
    m.h = h;
    m.data = (int*)malloc((size_t)w * (size_t)h * sizeof(int));
    if (!m.data) {
        perror("malloc");
        exit(1);
    }
    // Mirror the C++ constructor: data[i*w + j] = i + j
    for (int i = 0; i < h; ++i) {
        for (int j = 0; j < w; ++j) {
            if (initempty) {
                m.data[i * w + j] = 0;
            } else {
                m.data[i * w + j] = i + j;
            }
        }
    }
    return m;
}

static inline int matrix_gt(const Matrix *m, int x, int y) {
    // Mirrors data.at(x * w + y) bounds-checked access.
    assert(x >= 0 && x < m->h);
    assert(y >= 0 && y < m->w);
    return m->data[x * m->w + y];
}

static inline void matrix_st(Matrix *m, int x, int y, int val) {
    // Mirrors data.at(x * w + y) bounds-checked access.
    assert(x >= 0 && x < m->h);
    assert(y >= 0 && y < m->w);
    m->data[x * m->w + y] = val;
}

static void matrix_free(Matrix *m) {
    free(m->data);
    m->data = NULL;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "usage: %s <M>\n", argv[0]);
        return 1;
    }

    int M = (int)atol(argv[1]);
    int N = M;
    int K = N;

    Matrix a = matrix_new(M, N, 0);
    Matrix b = matrix_new(N, K, 0);
    Matrix c = matrix_new(M, K, 1);

    int64_t t1 = now_us();

    // NOTE: This loop mirrors your C++ exactly:
    // c.st(m,k, a.gt(m,k) * b.gt(k,n) + c.gt(m,n));
    // (Yes, indices are "unusual" for standard matmul, but kept identical.)
    for (int m = 0; m < M; m++) {
        for (int n = 0; n < N; n++) {
            for (int k = 0; k < K; k++) {
                int val = matrix_gt(&a, m, k) * matrix_gt(&b, k, n) + matrix_gt(&c, m, n);
                matrix_st(&c, m, n, val);
            }
        }
    }

    puts("out");

    int64_t t2 = now_us();

    // Keep a value to prevent over-optimization and mirror the C++ output
    printf("%d\n", matrix_gt(&c, M - 1, K - 1));
    printf("runtime: %lld µs\n", (long long)(t2 - t1));

    matrix_free(&a);
    matrix_free(&b);
    matrix_free(&c);
    return 0;
}
