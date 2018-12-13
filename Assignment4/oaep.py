import hashlib
import math

def main():
    print("apa")
    mgfSeed = "0123456789abcdef"  # (hexadecimal)
    maskLen = 30  # (decimal)
    output = "18a65e36189833d99e55a68dedda1cce13a494c947817d25dc80d9b4586a"

    mgf1_ans = mgf1(mgfSeed, maskLen)


def mgf1(mgfSeed, maskLen):
    print("222apa")
    hlen = 20 # length for sha-1 in bytes (octets)
    if maskLen > 2**32 * hlen:
        print("mask too long")
        return 0
    else:
        octetString = ""
        c = int(math.ceil((maskLen/hlen)))
        print("range",c)
        for counter in range(0,c):
            print("isk")
            counter_octet = convertToOctet(counter)
            octetString = octetString + hash(mgfSeed + counter_octet)
    return 0

def convertToOctet(val):
    print("apa")
    xLen = 4
    if val < 0:
        return ValueError("no negative integers")
    elif val > 256 ** xLen: #length of 4 octets
        return ValueError("integer to large")
    else:
        octet = hex(val)[2:].zfill(xLen *2)
        print("octet",octet)
        return octet.decode('UTF-8')

def hash(string):
    sha1 = hashlib.sha1()
    sha1.update(string.encode('UTF-8'))
    hashValue = sha1.hexdigest()
    return hashValue

main()
