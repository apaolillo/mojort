import time
from sys.arg import argv

struct Matrix:
    var data: List[Int]
    var w:Int
    var h:Int

    fn __init__(out self, width: Int, height: Int,initempty:Bool):
        self.data = List[Int](capacity=width*height)
        self.w = width
        self.h = height

        for i in range(height):
            for j in range(width):
                if initempty:
                    self.data[i * width + j] = 0
                else:
                    self.data[i * width + j] = i + j

    fn gt(self, x: Int ,y: Int) -> Int:
        return self.data[x * self.w + y]

    fn st(mut self, x: Int ,y: Int ,val: Int):
        self.data[x * self.w + y] = val



def main():
    var M = atol(argv()[1])
    var N = M
    var K = N
    var a = Matrix(M,N,False)
    var b = Matrix(N,K,False)
    var c = Matrix(M,K,True)
    var t1 = time.monotonic() / 1000
    for m in range(M):
        for n in range(N):
            for k in range(K):
                c.st(m,n,a.gt(m,k)*b.gt(k,n)+c.gt(m,n))
    var t2 = time.monotonic() / 1000
    var diff = (t2 -t1)
    # printing the corner element of the matrix
    # done so the compiler wont remove the workload
    var check = c.gt(M-1,N-1)
    print(String("checkvalue: {}").format(String(check)))
    print(String("runtime: {} µs").format(String(diff)))
