import time
import ssl
import statistics
from urllib.request import urlopen


def buildSignature(url):
    signature = ""
    while (len(signature) < 20):
        elapsed_longest = 0.0
        bestHex = ""
        tries = 6 + (3 * len(signature))

        for testValue in range(0, 16):
            hexValueToAdd = hex(testValue)[2:]
            print("----------------------------")
            print("Trying to add:", hexValueToAdd)

            newUrl = url + signature + hexValueToAdd
            elapsedVector = []
            for t in range(0, tries):
                start_time = time.time()
                urlopen(newUrl, context=ssl._create_unverified_context())
                fin_time = time.time()
                elapsed_time = fin_time - start_time
                elapsedVector.append(elapsed_time)
            elapsed_min = min(elapsedVector)
            print("Total elapsed:", elapsed_min)
            if elapsed_min > elapsed_longest:
                elapsed_longest = elapsed_min
                bestHex = hexValueToAdd
        signature += bestHex

        print("----------------------------")
        print("******************************")
        print("adding to signature:", bestHex)
        print("total signature:", signature)
        print("correct: 6823ea50b133c58cba36")
        print("******************************")
        print()
        print()

    return signature


def attack(name, grade):
    basic_url = "https://eitn41.eit.lth.se:3119/ha4/addgrade.php?"
    target_url = "name="+name+"&grade="+str(grade)+"&signature="
    url = str(basic_url) + str(target_url)

    signature = buildSignature(url)

    correct_url = url + signature
    print("Correct url:", correct_url)
    print("Correct signature:", signature)
    return correct_url


totalt_time_start = time.time()
signature = attack("Kalle", 5)
totalt_time_fin = time.time()
print()
print("---------------------------------------")
print("ANSWER")
print("Signature:", signature)
print("Total time:", round(totalt_time_fin-totalt_time_start, 2))
