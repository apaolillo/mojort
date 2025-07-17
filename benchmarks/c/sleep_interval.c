#include <stdio.h>
#include <time.h>
#include <unistd.h>

double monotonic_time_sec() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec / 1e9;
}

int main() {
    const double interval = 0.01;  // 10ms
    const int iterations = 50;
    double total_latency = 0.0;

    for (int i = 0; i < iterations; i++) {
        double expected = monotonic_time_sec() + interval;

        // Sleep for 10ms
        struct timespec sleep_time;
        sleep_time.tv_sec = 0;
        sleep_time.tv_nsec = (long)(interval * 1e9);
        nanosleep(&sleep_time, NULL);

        double actual = monotonic_time_sec();
        double latency = (actual - expected) * 1e6;  // in microseconds

        printf("Iteration %d: Latency = %.2f µs\n", i, latency);
        total_latency += latency;
    }

    printf("Total latency: %.2f µs\n", total_latency);
    return 0;
}
