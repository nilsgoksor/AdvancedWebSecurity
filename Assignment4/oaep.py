

def main():
    mgfSeed = "0123456789abcdef"  # (hexadecimal)
    maskLen = 30  # (decimal)
    output = "18a65e36189833d99e55a68dedda1cce13a494c947817d25dc80d9b4586a"

    mgf1_ans = mgf1(mgfSeed, maskLen)


def mgf1(mgfSeed, maskLen):
    if maskLen > 2**32:
        print("mask too long")
        return 0
    else:

    return 0
