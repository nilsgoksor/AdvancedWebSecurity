import sys
import hashlib
import math


def stringToBytes(s):
    byt = bytes.fromhex(s)
    return(byt)


def shaHash(nbr):
    hashf = hashlib.sha1()
    hashf.update(nbr)
    hash = hashf.hexdigest()
    return(hash)


def readFromFile(filePath):
    try:
        file = open(filePath, 'r')
        lines = file.readlines()
    finally:
        file.close()
    return lines


def merklePath(path):
    nodes = readFromFile(path)
    node = nodes[0]
    for i in range(1, len(nodes), 1):
        sibling = nodes[i]
        head, tail = sibling[0], sibling[1:]
        if head == 'L':
            concat = str(tail) + str(node)
            # print("L")
            # print(concat)
        else:
            concat = str(node) + str(tail)
            # print("R")
            # print(concat)
        byteNode = stringToBytes(concat)
        node = shaHash(byteNode)
        #print("Hash :", node)
    print("Last node: ", node)


def createMerklePath(path):
    nodes = readFromFile(path)
    indexToFind, returnDepth = nodes[0], nodes[1]
    nodes = nodes[2:]
    level = math.ceil(math.log2(len(nodes)))
    tempList = []
    answer = ""
    for depth in range(level, 0, -1):
        for index in range(len(nodes)):
            if(index % 2 == 0):
                # left
                # copy
                if(index == len(nodes)-1):
                    concat = nodes[index] + nodes[index]
                else:
                    concat = nodes[index] + nodes[index+1]
                byteNode = stringToBytes(concat)
                node = shaHash(byteNode)
                tempList.append(node)
                # check
                if index == indexToFind:
                    node = nodes[index+1]
                    node = "R" + node[:40]
                    if int(depth) == int(returnDepth):
                        answer = node
            else:
                # right - only check
                if int(index) == int(indexToFind):
                    node = nodes[index-1]
                    node = "L" + node[:40]
                    if int(depth) == int(returnDepth):
                        answer = node

        nodes = tempList
        tempList = []
        indexToFind = round(int(indexToFind)/2)
    answer = answer + nodes[0]
    print(answer)
