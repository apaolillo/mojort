use std::env;
use std::time::Instant;

const LIMIT: i32 = 1000;

#[inline]
fn mandelbrot_split(real: f64, imag: f64) -> i32 {
    let (mut zr, mut zi) = (real, imag);
    for i in 0..LIMIT {
        let r2 = zr * zr;
        let i2 = zi * zi;
        if r2 + i2 > 4.0 {
            return i;
        }
        zi = 2.0 * zr * zi + imag;
        zr = r2 - i2 + real;
    }
    LIMIT
}

fn main() {
    let width: usize = env::args()
        .nth(1)
        .expect("usage: mandelbrot <width>")
        .parse()
        .expect("width must be a positive integer");
    let height = width;

    let x_start = -2.0_f64;
    let x_fin = 0.47_f64;
    let y_start = -1.12_f64;
    let y_fin = 1.12_f64;

    let dx = (x_fin - x_start) / (width as f64 - 1.0);
    let dy = (y_fin - y_start) / (height as f64 - 1.0);

    let t0 = Instant::now();
    let mut a: i64 = 0;

    for i in 0..height {
        for j in 0..width {
            let x = x_start + (j as f64) * dx; // real
            let y = y_fin - (i as f64) * dy;   // imag
            a += mandelbrot_split(x, y) as i64;
        }
    }

    let us = t0.elapsed().as_micros();

    // printing "a" the sum of all element in the mandelbrot matrix
    // done so the compiler wont remove the workload
    println!("checkvalue: {}", a);
    println!("runtime: {} µs", us);
}
