

# errno is not accesble
# https://github.com/modular/modular/issues/2532

import sys
import runtime
from algorithm.functional import parallelize
from time import sleep

struct _CTimeSpec(Copyable, Defaultable, Movable, Stringable, Writable):
    var tv_sec: Int  # Seconds
    var tv_nsec: Int  # subsecond (nanoseconds on linux and usec on mac)

    fn __init__(out self):
        self.tv_sec = 0
        self.tv_nsec = 0

    fn as_nanoseconds(self) -> UInt:
        return self.tv_sec * 1000 * 1000 * 1000 + self.tv_nsec

    @no_inline
    fn __str__(self) -> String:
        return String.write(self)

    @no_inline
    fn write_to[W: Writer](self, mut writer: W):
        writer.write(self.as_nanoseconds(), "ns")

struct _schedParam(Copyable, Defaultable, Movable, Stringable, Writable):
    var sched_priority:Int

    fn __init__(out self):
        self.sched_priority = 99

    @no_inline
    fn __str__(self) -> String:
        return String.write(self)

    @no_inline
    fn write_to[W: Writer](self, mut writer: W):
        writer.write(self.sched_priority)

def test():
    var ts = _CTimeSpec()
    r = sys.external_call["clock_gettime", Int32](Int32(0), Pointer(to=ts))
    # r = sys.external_call["clock_nanosleep", Int32](Int32(0), Pointer(to=ts))
    print(r)
    print(ts)

def test2():
    var param = _schedParam()
    # sched_setscheduler(0, SCHED_FIFO, [1])  = -1 EPERM (Operation not permitted) -> strace
    # docker container needs to be priveliged and needs to be run with sudo

    r = sys.external_call["sched_setscheduler", Int32](Int(0),Int(1), Pointer(to=Int(1)))
    # r = sys.external_call["sched_getscheduler", Int32](Int(0))
    print(r)

def get_time_sys(ts:_CTimeSpec):
    _ = sys.external_call["clock_gettime", Int32](Int32(1), Pointer(to=ts))

var CLOCK_MONOTONIC = 1
var TIMER_ABSTIME = 1

def nanosleep_sys(sp:_CTimeSpec):
    var ts = _CTimeSpec()
    _ = sys.external_call["clock_nanosleep", Int32](Int32(CLOCK_MONOTONIC), Int(TIMER_ABSTIME), Pointer(to=sp),Pointer(to=ts))

def threadstart():
    @parameter
    fn timer_thread(i:Int) -> None:
        try:

            test2()
            var ts = _CTimeSpec()
            var runtime = 2 * 1000 * 1000 * 1000
            var done = False
            var start_time = _CTimeSpec()
            var new_time = _CTimeSpec()
            get_time_sys(start_time)
            var current_time = start_time
            while not done:
                get_time_sys(current_time)
                if current_time.as_nanoseconds() - start_time.as_nanoseconds() > runtime:
                    done = True
                get_time_sys(current_time)
                ts = current_time
                # TODO: this needs to have a rolover thing
                ts.tv_nsec = ts.tv_nsec + 1 * 1000 * 1000
                nanosleep_sys(ts)
                get_time_sys(new_time)
                print(new_time.as_nanoseconds() - current_time.as_nanoseconds())
        except e:
            pass

    parallelize[timer_thread](1)

# showing that parallelization is not spawing new threads
def parallel_not():
    @parameter
    fn getpid(i:Int):
        r = sys.external_call["gettid",Int32]()
        sleep(UInt(1))
        print(r)
    parallelize[getpid](400)

def main():
    try:
        threadstart()
    except e:
        pass