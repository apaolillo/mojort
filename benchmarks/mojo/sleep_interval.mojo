import time

def main():
    var interval = 0.01  # 10ms
    var iterations = 50
    var total_latency = 0.0

    for i in range(iterations):
        var expected = (time.monotonic()/1e9) + interval
        time.sleep(interval)
        var actual = time.monotonic() / 1e9
        var latency = (actual - expected) * 1_000_000  # µs
        var s = String("Iteration {0}: Latency = {1} µs").format(String(i), String(latency))
        print(s)
        expected += interval
        total_latency += latency
    print(String("Total latency: {} µs").format(String(total_latency)))
