from sys.ffi import external_call

# Constants
alias UART_BASE:    UInt64 = 0x0900_0000
alias UART_DR_ADDR: UInt64 = UART_BASE + 0x00
alias UART_FR_ADDR: UInt64 = UART_BASE + 0x18
alias UART_FR_TXFF: UInt32 = 1 << 5  # TX FIFO full

# Call the C shims
fn mmio_read32(addr: UInt64) -> UInt32:
    return external_call["mmio_read32", UInt32, UInt64](addr)

fn mmio_write32(addr: UInt64, value: UInt32) -> None:
    external_call["mmio_write32", NoneType, UInt64, UInt32](addr, value)

# Mojo implementation of uart_send
@export("uart_send", ABI="C")
fn uart_send(c: UInt8) -> None:
    while (mmio_read32(UART_FR_ADDR) & UART_FR_TXFF) != 0:
        pass
    mmio_write32(UART_DR_ADDR, UInt32(c))

"""
# Try this import first:
from memory import UnsafePointer
# If your build doesn't have sys.memory, try:
# from memory import UnsafePointer

# PL011 on QEMU virt
alias UART_BASE:    UInt64 = 0x0900_0000
alias UART_DR_ADDR: UInt64 = UART_BASE + 0x00
alias UART_FR_ADDR: UInt64 = UART_BASE + 0x18
alias UART_FR_TXFF: UInt32 = 1 << 5  # TX FIFO full

fn mmio_read32(addr: UInt64) -> UInt32:
    var p = UnsafePointer[UInt32].from_address(addr)
    return p.load_volatile()

fn mmio_write32(addr: UInt64, value: UInt32) -> None:
    UnsafePointer[UInt32].from_address(addr).store_volatile(value)

@export("uart_send", ABI="C")
fn uart_send(c: UInt8) -> None:
    while (mmio_read32(UART_FR_ADDR) & UART_FR_TXFF) != 0:
        pass
    mmio_write32(UART_DR_ADDR, UInt32(c))
"""
