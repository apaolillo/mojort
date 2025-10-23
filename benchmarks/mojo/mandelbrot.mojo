from complex import ComplexFloat64, abs
from sys.arg import argv
import time

alias MAX_ITERS = 1000

fn mandelbrot_complex(c: ComplexFloat64) -> Int:
    var z = c
    var nv = 0
    for _ in range(0, MAX_ITERS):
      if abs(z) > 2:
        break
      z = z*z + c
      nv += 1
    return nv

fn mandelbrot_split(real: Float64, imag: Float64) -> Int:
  var nv = 0
  var zReal:Float64 = real
  var zImag:Float64 = imag
  for _ in range(0, MAX_ITERS):
    var r2:Float64 = zReal * zReal
    var i2:Float64 = zImag * zImag
    if r2 + i2 > 4.0:
      break
    zImag = 2.0 * zReal * zImag + imag
    zReal = r2 - i2 + real
  return nv

alias min_x = -2.0
alias max_x = 0.47
alias min_y = -1.12
alias max_y = 1.12

def main():
  # arguments
  # 1) size
  var width:Int = atol(argv()[1])
  var height = width
  var scale_x = (max_x - min_x) / (width - 1)
  var scale_y = (max_y - min_y) / (height - 1)
  var a = 0

  var t1 = time.monotonic() / 1000
  for h in range(height):
      var cy = max_y - h * scale_y
      for w in range(width):
          var cx = min_x + w * scale_x
          a =  a + mandelbrot_complex(ComplexFloat64(cx,cy))
          # a =  a + mandelbrot_split(cx,cy)
  var t2 = time.monotonic() / 1000
  var diff = (t2 -t1)
  # printing "a" the sum of all element in the mandelbrot matrix
  # done so the compiler wont remove the workload

  print(String("checkvalue: {}").format(String(a)))
  print(String("runtime: {} µs").format(String(diff)))
