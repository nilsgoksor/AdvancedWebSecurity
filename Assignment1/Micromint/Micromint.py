import numpy as np
import random
import statistics


def simulation(u, k, c):
    # Calculate amount of bins. Initiate a vector with this length containing 0s
    nbrBins = 2 ** u
    coinVector = [0] * nbrBins
    currentCointAmount = 0
    itr = 0
    # Throw while current coints is less than the goal. Increase currentCoint when a bin get k coins. keep track of itr amount
    while (currentCointAmount < c):
        randomBin = random.randint(0, nbrBins-1)  # -1 ??? TODO CHECK
        coinVector[randomBin] += 1
        if(coinVector[randomBin] == k):
            currentCointAmount += 1
        itr += 1
    return itr


def calculateAverageIterations(n, u, k, c):
    totalItr = 0
    itrVector = []
    for i in range(0, n):
        currentItr = simulation(u, k, c)
        totalItr += currentItr
        itrVector.append(currentItr)
    return totalItr / n, itrVector


def calculateConfidenceWidth(x_mean, n, stdDeviation):
    lamba = 3.66
    print("lamba:", lamba, "stDev:", stdDeviation, "n:", n)
    width = (lamba * stdDeviation / (n ** (1/2)))
    return width


# MAIN
n = 13
u = 20
k = 7
c = 10000

avgItrAmount, itrVector = calculateAverageIterations(n, u, k, c)
stdDeviation = statistics.stdev(itrVector)

width = calculateConfidenceWidth(avgItrAmount, n, stdDeviation)
print("Coins: ", c, "x_mean: ", avgItrAmount, "width: ", width)
