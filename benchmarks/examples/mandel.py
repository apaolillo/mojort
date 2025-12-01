MAX_ITERS = 1000


def mandelbrot_split(
    real: float,
    imag: float,
) -> int:
    nv = 0
    z_real = real
    z_imag = imag
    for _ in range(MAX_ITERS):
        r2 = z_real * z_real
        i2 = z_imag * z_imag
        if r2 + i2 > 4.0:
            break
        z_imag = 2.0 * z_real * z_imag + imag
        z_real = r2 - i2 + real
    return nv


if __name__ == "__main__":
    print(mandelbrot_split(-0.5, 0.0))
