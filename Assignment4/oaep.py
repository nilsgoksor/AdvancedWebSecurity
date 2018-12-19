import hashlib
import math


def main():
    # MGF1
    mgfSeed = "46dad84c7fa3460344bda67c31e8f948addb0649f13b7509"
    maskLen = 24
    mgf1_ans = mgf1(mgfSeed, maskLen)
    print("MGF1:", mgf1_ans)
    print()

    # ENCODE
    message = "30c34580753883e1f421f3a012476e14b25afed894448d65aa"
    seed = "1e652ec152d0bfcd65190ffc604c0933d0423381"
    encoded_m = oaep_encode(message, seed)
    print("Encode", encoded_m)
    print()

    # DECODE
    encoded_m = "00451e66a5e9b51f00abe919cfa277b237008087def9d3778a18b7aa067f90b2178406fa1e1bf77f03f86629dd5607d11b9961707736c2d16e7c668b367890bc6ef1745396404ba7832b1cdfb0388ef601947fc0aff1fd2dcd279dabdf472023d44ef55c4a40d1ce16608342d9b31f7fab5270ff56cf8f962258890b9f78184c"
    decoded_m = oaep_decode(encoded_m)
    print("Decode", decoded_m)


def mgf1(mgfSeed, maskLen):
    hlen = 20  # length for sha-1 in bytes (octets)
    if maskLen > 2**32 * hlen:
        print("mask too long")
        return 0
    else:
        octetString = ""
        c = int(math.ceil(maskLen/hlen))
        for counter in range(0, c):
            counter_octet = convertToOctet(counter, 4)
            octetString += hashlib.sha1(bytearray.fromhex(mgfSeed + counter_octet)
                                        ).hexdigest()

    return octetString[:maskLen*2]


def convertToOctet(val, xLen):
    if val < 0:
        return ValueError("no negative integers")
    elif val >= 256 ** xLen:  # length of 4 octets
        return ValueError("integer to large")
    octet = hex(val)[2:].zfill(xLen * 2)
    return octet


def oaep_encode(message, seed):
    L = ""
    l_hash = hashlib.sha1(bytearray.fromhex(L)).hexdigest()
    k = int(1024/8)
    hLen = int(len(l_hash)/2)
    mLen = len(message)

    ps = convertToOctet(0, int(k - mLen/2 - 2*hLen - 2))
    db = l_hash + ps + "01" + message

    db_mask = mgf1(seed, k-hLen-1)
    maskedDB = hex(int(db, 16) ^ int(db_mask, 16))[2:]

    seed_mask = mgf1(maskedDB, hLen)
    maskedSeed = hex(int(seed, 16) ^ int(seed_mask, 16))[2:]

    em = (maskedSeed+maskedDB).zfill(k * 2)
    return em


def oaep_decode(em):
    L = ""
    l_hash = hashlib.sha1(bytearray.fromhex(L)).hexdigest()
    k = int(1024/8)
    hLen = int(len(l_hash)/2)

    # Split em
    Y = em[:2]
    maskedSeed = em[2:hLen*2+2]
    maskedDB = em[hLen*2+2:]

    # Create seedmask and seed
    seedMask = mgf1(maskedDB, hLen)
    seed = hex(int(maskedSeed, 16) ^ int(seedMask, 16))[2:]

    # Create dbMask and db
    dbMask = mgf1(seed, k-hLen-1)
    db = hex(int(maskedDB, 16) ^ int(dbMask, 16))[2:]

    # Split db (db = l_hash + ps + "01" + message)
    indexOf01 = hLen * 2 + db[hLen * 2:].find("01")
    message = db[indexOf01+2:]
    return message


main()
