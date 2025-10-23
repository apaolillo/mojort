// https://github.com/dario-marvin/Mandelbrot/blob/master/Mandelbrot.cc

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <complex>
#include <cmath>

#include <chrono>

using namespace std;
typedef complex<double> fcomp;

int mandelbrotComplex(fcomp c) {
    int limit = 1000;
    fcomp z = c;

    for (int i = 0; i < limit; ++i) {
        if (abs(z) > 2) return i;
        z = z * z + c;
    }
    return limit;
}

int mandelbrotSplit(double real, double imag) {
    int limit = 1000;
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


int main(int argc, char *argv[]){
    using std::chrono::high_resolution_clock;
    using std::chrono::duration_cast;
    using std::chrono::duration;
    using std::chrono::milliseconds;

    int width = atol(argv[1]); //number of characters fitting horizontally on my screen
    int heigth = width; //number of characters fitting vertically on my screen

    double x_start = -2.0;
    double x_fin = 0.47;
    double y_start = -1.12;
    double y_fin = 1.12;

    double dx = (x_fin - x_start)/(width - 1);
    double dy = (y_fin - y_start)/(heigth - 1);

    auto t1 = high_resolution_clock::now();
    auto a = 0;
    for (int i = 0; i < heigth; i++) {
        for (int j = 0; j < width; j++) {

            double x = x_start + j*dx; // current real value
            double y = y_fin - i*dy; // current imaginary value

            // cout << mandelbrotComplex(fcomp(x,y)) << '\n';
            // cout << mandelbrotSplit(x,y) << '\n';

            a = a + mandelbrotComplex(fcomp(x,y));
            // a = a + mandelbrotSplit(x,y);
        }
    }
    auto t2 = high_resolution_clock::now();

    /* Getting number of milliseconds as a double. */
    duration<double, std::milli> ms_double = t2 - t1;
    // printing "a" the sum of all element in the mandelbrot matrix
    // done so the compiler wont remove the workload
    std::cout << "checkvalue: " << int(a) << "\n";
    std::cout << "runtime: " << int((ms_double.count() * 1000)) << " µs\n";
    return 0;
}
