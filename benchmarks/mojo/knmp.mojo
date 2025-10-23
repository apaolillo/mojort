import time
from sys.arg import argv

def computeLPSArray(pattern: String, m:Int) -> List[Int]:
    var LPS:List[Int] = List[Int](capacity=m)
    var length = 0
    var i = 1
    LPS[0] = 0

    while (i < m):
        if (pattern[i] == pattern[length]):
            length += 1
            LPS[i] = length
            i += 1
        else:
            if not (length == 0):
                length = LPS[length - 1]
            else:
                LPS[i] = 0
                i += 1

    return LPS

def KMP(pattern:String,text:String) -> List[Int]:
    var m:Int = len(pattern)
    var n:Int = len(text)
    var ans: List[Int] = List[Int]()
    var LPS: List[Int] = computeLPSArray(pattern,m)

    var i = 0
    var j = 0

    while (i<n):
        if (pattern[j] == text[i]):
            i += 1
            j += 1

        if (j == m):
            ans.append(i -j)
            j = LPS[j -1]

        else:
            if (i<n and (not (pattern[j] == text[i]))):
                if(not j == 0):
                    j = LPS[j -1]
                else:
                    i += 1
    return ans

def main():
    var  f = open("../the_bible.txt", "r")
    var bible = f.read()

    var p = atof(argv()[1])
    var ln = len(bible)
    var newlen:Int = Int(ln * p)

    bible = bible[0:newlen]

    var t1 = time.monotonic() / 1000
    var l = KMP('God',bible)
    var t2 = time.monotonic() / 1000
    var diff = (t2 -t1)
    # printing the index of the last found match
    # done so the compiler wont remove the workload
    var check = l[len(l)-1]
    print(String("checkvalue: {}").format(String(check)))
    print(String("runtime: {} µs").format(String(diff)))
