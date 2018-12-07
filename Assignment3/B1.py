import hashlib
import matplotlib.pyplot as plt
import numpy as np


def hash(string):
    sha1 = hashlib.sha1()
    sha1.update(string.encode('UTF-8'))
    hashValue = sha1.hexdigest()
    binaryValue = bin(int(hashValue, 16))
    return binaryValue

def getBindingProbability(K):
    length = 2**K - 1
    x = 1
    probabilityVector = []
    concatVector = []

    # Calculates the bindng-probability and increments truncate-Length x until we get timesBroken = 0
    searching = True
    while searching:
        timesBroken = 0
        # For each integer k in range 0 to length, concat it with v=0 and v=1 and hash each.
        # If both are equal, we increment timesBroken
        for k in range(0, length):
            string_v0 = str(0) + str(k)
            string_v1 = str(1) + str(k)
            hash_v0 = hash(string_v0)
            hash_v1 = hash(string_v1)
            if str(hash_v0)[2:x] == str(hash_v1)[2:x]:
                timesBroken += 1
                break

        # If timesBroken > 0, the broken probability = 1.
        if timesBroken == 0:
            searching = False
            probabilityVector.append(0)
        else:
            probabilityVector.append(1)
            x += 1

    for i in range(1, x+1):
        concatVector.append(i)

    # We plot the broken probability for each concatLenght until we get probability 0
    plt.plot(concatVector, probabilityVector, 'o')
    plt.ylabel('probability - binding')
    plt.xlabel('truncation length - x')
    plt.show()
    return probabilityVector


def getConcealingProbability(K, x, receivedHash):
    length = 2**K - 1
    collisionCounter_v0 = 0
    collisionCounter_v1 = 0
    for k in range(0, length):
        # Create two hashes, one for v = 0 and one for v = 1
        string_v0 = str(0) + str(k)
        string_v1 = str(1) + str(k)
        hash_v0 = hash(string_v0)
        hash_v1 = hash(string_v1)

        # Is there a match between hash for v=0 and receivedHash
        if hash_v0[2:x] == receivedHash[2:x]:
            collisionCounter_v0 += 1

        # Is there a match between hash for v=1 and receivedHash
        if hash_v1[2:x] == receivedHash[2:x]:
            collisionCounter_v1 += 1
    
    print(collisionCounter_v0, " - ", collisionCounter_v1) 
    # Returns the concealing probability, which is 1 if we found collisions for v0 or v1, and none for the other
    if collisionCounter_v0 > 0 and collisionCounter_v1 == 0 or collisionCounter_v1 > 0 and collisionCounter_v0 == 0:
        return 1
    
    return 0

def sentByAlice(K):
    # A randomized hash wich we pretends Alice sends
    v = np.random.randint(2, size=1)[0]
    k = np.random.randint((2**K)-1, size=1)[0]
    h = hash(str(v)+str(k))
    return h

def visualizeConcealingProb(K):
    x = 1 # truncate length
    xVector = []
    probVector = []
    receivedHash = sentByAlice(K)

    # getConcealingProbability 10 times
    for x in range(1, 40):
        xVector.append(x)
        probVector.append(getConcealingProbability(K, x, receivedHash))

    # Plots the concealing prob, returns the values
    plt.plot(xVector, probVector)
    plt.ylabel('probability - concealed')
    plt.xlabel('x')
    plt.show()
    return probVector


K = 16
print("Binding prob vector:", getBindingProbability(K))
#print("Concealing prob:", visualizeConcealingProb(K))
