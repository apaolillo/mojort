#include <vector>
#include <iostream>
#include <chrono>
using namespace std;


class Matrix {
        vector<int>  data;
    public:
        int w,h;
        Matrix(int wi,int hi,bool initempty) {
            w = wi;
            h = hi;
            data = std::vector<int>(w*h);
            for (int i = 0; i < h; i++) {
                for (int j = 0; j < w; j++) {
                    if (initempty) {
                        data.at(i * w + j) = 0;
                    } else {
                        data.at(i * w + j) = i + j;
                    }
                }
            }
        ;}
        int gt(int x,int y) {
            return data.at(x * w + y);
        }
        void st(int x, int y, int val) {
            data.at(x * w + y) = val;
        }
};

int main(int argc, char *argv[]) {
    using std::chrono::high_resolution_clock;
    using std::chrono::duration_cast;
    using std::chrono::duration;
    using std::chrono::milliseconds;
    int M = atol(argv[1]);
    int N = M;
    int K = N;
    Matrix a = Matrix(M,N,false);
    Matrix b = Matrix(N,K,false);
    Matrix c = Matrix(M,K,true);

    auto t1 = high_resolution_clock::now();
    for (int m = 0; m < M; m++) {
        for (int n = 0; n < N; n++) {
            for (int k = 0; k < K; k++) {
                c.st(m,n,a.gt(m,k)*b.gt(k,n)+c.gt(m,n));
            }
        }
    }
    std::cout << "out" << '\n';

    auto t2 = high_resolution_clock::now();

    /* Getting number of milliseconds as a double. */
    duration<double, std::milli> ms_double = t2 - t1;
    // printing a otherwise the compiler will optimize the loop away
    std::cout << c.gt(M-1,K-1) << '\n';
    std::cout << "runtime: " << int((ms_double.count() * 1000)) << " µs\n";
    return 0;
}
