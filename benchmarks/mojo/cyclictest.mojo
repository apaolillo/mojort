# errno is not accesble
# https://github.com/modular/modular/issues/2532

import sys
import runtime
from algorithm.functional import parallelize
from time import sleep
from sys.arg import argv

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

def set_scheduling_policy():
    # sched_setscheduler(0, SCHED_FIFO, [1])  = -1 EPERM (Operation not permitted) -> strace
    # docker container needs to be priveliged and needs to be run with sudo

    r = sys.external_call["sched_setscheduler", Int32](Int(0),Int(1), Pointer(to=Int(99)))

def lock_pages():
    r = sys.external_call["mlockall", Int32](Int(3))

def unlock_pages():
    r = sys.external_call["munlockall", Int32]()

def get_time_sys(ts:_CTimeSpec):
    _ = sys.external_call["clock_gettime", Int32](Int32(1), Pointer(to=ts))


var RUNTIME_SEC = 60
var SEC_MULTIPLIER = 1000 * 1000 * 1000

var CLOCK_MONOTONIC = 1
var TIMER_ABSTIME = 1

def nanosleep_sys(sp:_CTimeSpec):
    var ts = _CTimeSpec()
    _ = sys.external_call["clock_nanosleep", Int32](Int32(CLOCK_MONOTONIC), Int(TIMER_ABSTIME), Pointer(to=sp),Pointer(to=ts))

def threadstart():
    @parameter
    fn timer_thread(i:Int) -> None:
        var intervals = [100,600,1100,1600]
        var interval = intervals[i]
        var iter = 0
        try:
            set_scheduling_policy()
            new_nsec = 0
            var ts = _CTimeSpec()
            var runtime = RUNTIME_SEC * SEC_MULTIPLIER
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
                new_nsec = ts.tv_nsec + interval
                if new_nsec > SEC_MULTIPLIER:
                    new_nsec = new_nsec - SEC_MULTIPLIER
                    ts.tv_sec = ts.tv_sec + 1
                ts.tv_nsec = new_nsec
                nanosleep_sys(ts)
                get_time_sys(new_time)
                var diff:Int32 = new_time.as_nanoseconds() - current_time.as_nanoseconds() - interval
                p = String(i) + ":\t" + String(iter) + ":\t" + String(diff)
                print (p)
                iter = iter + 1
        except e:
            pass

    parallelize[timer_thread](atol(argv()[1]))

def main():
    try:
        if len(argv()) > 2:
            lock_pages()
        threadstart()
        if len(argv()) > 2:
            unlock_pages()
    except e:
        print(e)
