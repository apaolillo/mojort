import time
from sys.arg import argv

struct Matrix:
    var data: List[Int]
    var w:Int
    var h:Int

    fn __init__(out self, width: Int, height: Int):
        self.data = List[Int](capacity=width*height)
        self.w = width
        self.h = height

        for i in range(height):
            for j in range(width):
                self.data[i * width + j] = i + j

    fn gt(self, x: Int ,y: Int) -> Int:
        return self.data[x * self.w + y]

    fn st(mut self, x: Int ,y: Int ,val: Int):
        self.data[x * self.w + y] = val



def main():
    var M = atol(argv()[1])
    var N = M
    var K = N
    var a = Matrix(M,N)
    var b = Matrix(N,K)
    var c = Matrix(M,K)
    var t1 = time.monotonic() / 1000
    for m in range(M):
        for n in range(N):
            for k in range(K):
                c.st(m,k,a.gt(m,k)*b.gt(k,n)+c.gt(m,n))
    var t2 = time.monotonic() / 1000
    var diff = (t2 -t1)
    # printing otherwise the compiler will optimize the loop away
    print(c.gt(M-1,K-1))
    print(String("runtime: {} µs").format(String(diff)))
