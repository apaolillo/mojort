.global _vectors

.section .vector, "ax", %progbits   // Mark .vector as executable and allocated
.align 11                   // Align to 2 KB boundary (required by ARM spec)
_vectors:
.org 0x0000
    b .
.org 0x0080
    b .
.org 0x0100
    b .
.org 0x0180
    b .
.org 0x0200
    b el1_sync_handler
.org 0x0280
    b .
.org 0x0300
    b .
.org 0x0380
    b .
.org 0x0400
    b el1_svc_handler
.org 0x0480
    b irq_handler
.org 0x0500
    b .
.org 0x0580
    b .
.org 0x0600
    b .
.org 0x0680
    b .
.org 0x0700
    b .
.org 0x0780
    b .
