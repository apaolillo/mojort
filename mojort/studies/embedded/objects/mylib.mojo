# mylib.mojo

# Expose under a C-friendly name with the C calling convention
@export("add_ints", ABI="C")
fn add_ints(a: Int32, b: Int32) -> Int32:
    return a + b

@export("saxpy_scalar", ABI="C")
fn saxpy_scalar(a: Float64, x: Float64, y: Float64) -> Float64:
    # returns a*x + y — still just scalars, no arrays
    return a * x + y

@export("is_even", ABI="C")
fn is_even(n: Int32) -> Int32:
    # Return 1/0 like a classic C bool
    return 1 if (n % 2 == 0) else 0
