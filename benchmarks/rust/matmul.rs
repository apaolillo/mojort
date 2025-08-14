use std::env;
use std::time::Instant;

struct Matrix {
    w: usize,
    h: usize,
    data: Vec<i32>,
}

impl Matrix {
    fn new(w: usize, h: usize,initempty:bool) -> Self {
        let mut data = vec![0i32; w * h];
        // Mirrors: data[i*w + j] = i + j
        for i in 0..h {
            for j in 0..w {
                if initempty {
                    data[i * w + j] = 0 as i32;
                } else {
                    data[i * w + j] = (i + j) as i32;
                }
            }
        }
        Self { w, h, data }
    }

    #[inline]
    fn gt(&self, x: usize, y: usize) -> i32 {
        debug_assert!(x < self.h && y < self.w);
        self.data[x * self.w + y]
    }

    #[inline]
    fn st(&mut self, x: usize, y: usize, val: i32) {
        debug_assert!(x < self.h && y < self.w);
        self.data[x * self.w + y] = val;
    }
}

fn main() {
    let m: usize = env::args()
        .nth(1)
        .expect("usage: matrix <M>")
        .parse()
        .expect("M must be a positive integer");
    let n = m;
    let k = n;

    let a = Matrix::new(m, n,false);
    let b = Matrix::new(n, k,false);
    let mut c = Matrix::new(m, k,true);

    let t0 = Instant::now();

    // Mirrors exactly:
    // c.st(m,k, a.gt(m,k) * b.gt(k,n) + c.gt(m,n));
    for mi in 0..m {
        for ni in 0..n {
            for ki in 0..k {
                let val = a.gt(mi, ni) * b.gt(ki, ni) + c.gt(mi, ni);
                c.st(mi, ki, val);
            }
        }
    }

    println!("out");

    let us = t0.elapsed().as_micros();
    println!("{}", c.gt(m - 1, k - 1));
    println!("runtime: {} µs", us);
}
