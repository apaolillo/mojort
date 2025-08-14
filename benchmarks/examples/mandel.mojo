alias MAX_ITERS: Int = 1000

fn mandelbrot_split(
    real: Float64,
    imag: Float64,
) -> Int:
    var nv: Int = 0
    var zReal: Float64 = real
    var zImag: Float64 = imag
    for _ in range(0, MAX_ITERS):
        var r2: Float64 = zReal * zReal
        var i2: Float64 = zImag * zImag
        if r2 + i2 > 4.0:
            break
        zImag = 2.0 * zReal * zImag + imag
        zReal = r2 - i2 + real
    return nv

fn main():
    print(mandelbrot_split(-0.5, 0.0))
