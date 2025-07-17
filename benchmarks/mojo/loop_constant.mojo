def accumulate() -> Int:
    var acc: Int = 0
    for i in range(1_000_000):
        acc += i
    return acc

def main():
    var result: Int = accumulate()
    print(result)
