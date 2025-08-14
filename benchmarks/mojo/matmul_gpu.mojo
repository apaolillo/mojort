# ===----------------------------------------------------------------------=== #
# Copyright (c) 2025, Modular Inc. All rights reserved.
#
# Licensed under the Apache License v2.0 with LLVM Exceptions:
# https://llvm.org/LICENSE.txt
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===----------------------------------------------------------------------=== #

# https://www.quantstart.com/articles/Matrix-Matrix-Multiplication-on-the-GPU-with-Nvidia-CUDA/
# 312781568

from math import ceildiv
from sys import has_accelerator

from memory.unsafe_pointer import UnsafePointer

import time
from sys.arg import argv

from gpu.host import DeviceContext
from gpu.id import block_dim, block_idx, thread_idx
from layout import Layout, LayoutTensor

# Vector data type and size

# Calculate the number of thread blocks needed by dividing the vector size
# by the block size and rounding up.

alias int_dtype = DType.int64


fn matrix_mulitiplication(
    A: UnsafePointer[Int64],
    B: UnsafePointer[Int64],
    C: UnsafePointer[Int64],
    N:Int
):

    var ROW = block_idx.y*block_dim.y+thread_idx.y
    var COL = block_idx.x*block_dim.x+thread_idx.x

    if ((ROW < N)and (COL < N)):
        for i in range(N):
            C[ROW * N + COL] += A[ROW * N + i] * B[i * N + COL]


def main():
    var N = atol(argv()[1])
    var vector_size = N*N
    @parameter
    if not has_accelerator():
        print("No compatible GPU found")
    else:
        # Get the context for the attached GPU
        ctx = DeviceContext()

        # Create HostBuffers for input vectors
        lhs_host_buffer = ctx.enqueue_create_host_buffer[int_dtype](
            vector_size
        )
        rhs_host_buffer = ctx.enqueue_create_host_buffer[int_dtype](
            vector_size
        )
        ctx.synchronize()

        # Initialize the input vectors
        for i in range(N):
            for j in range(N):
                lhs_host_buffer[i * N + j] = i + j
                rhs_host_buffer[i * N + j] = i + j

        var t1 = time.monotonic() / 1000

        # Create DeviceBuffers for the input vectors
        lhs_device_buffer = ctx.enqueue_create_buffer[int_dtype](vector_size)
        rhs_device_buffer = ctx.enqueue_create_buffer[int_dtype](vector_size)

        # Copy the input vectors from the HostBuffers to the DeviceBuffers
        ctx.enqueue_copy(dst_buf=lhs_device_buffer, src_buf=lhs_host_buffer)
        ctx.enqueue_copy(dst_buf=rhs_device_buffer, src_buf=rhs_host_buffer)

        # Create a DeviceBuffer for the result vector
        result_device_buffer = ctx.enqueue_create_buffer[int_dtype](
            vector_size
        )

        # Wrap the DeviceBuffers in LayoutTensors
        # lhs_tensor = LayoutTensor[int_dtype, layout](lhs_device_buffer)
        # rhs_tensor = LayoutTensor[int_dtype, layout](rhs_device_buffer)
        # result_tensor = LayoutTensor[int_dtype, layout](result_device_buffer)

        # Compile and enqueue the kernel
        ctx.enqueue_function[matrix_mulitiplication](
            lhs_device_buffer,
            rhs_device_buffer,
            result_device_buffer,
            N,
            grid_dim=(N,N),
            block_dim=1,
        )

        # Create a HostBuffer for the result vector
        result_host_buffer = ctx.enqueue_create_host_buffer[int_dtype](
            vector_size
        )

        # Copy the result vector from the DeviceBuffer to the HostBuffer
        ctx.enqueue_copy(
            dst_buf=result_host_buffer, src_buf=result_device_buffer
        )

        ctx.synchronize()

        var t2 = time.monotonic() / 1000
        var diff = (t2 -t1)
        # printing otherwise the compiler will optimize the loop away

        var check:Int64 = result_host_buffer[vector_size - 1]
        print(String("checkvalue: {}").format(String(check)))
        print(String("runtime: {} µs").format(String(diff)))
