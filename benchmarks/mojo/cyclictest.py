import os
import subprocess
import sys

# this is a wrapper since mojo fails at editing '/dev/cpu_dma_latency'

try:
    fd = os.open('/dev/cpu_dma_latency', os.O_WRONLY)
    os.write(fd, b'\0\0\0\0')
    subprocess.run(['./cyclictest', sys.argv[1]])
    os.close(fd)

except:
    pass
