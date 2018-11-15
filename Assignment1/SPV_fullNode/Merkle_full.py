import hashlib
import math


def sha1function(byte_vector):
    sha1 = hashlib.sha1()
    sha1.update(byte_vector)
    return sha1.hexdigest()


def findPathOnLevel(nodes, i):
    if(i >= len(nodes)):
        return
    if(i % 2 == 0):
        if(len(nodes) <= i+1):
            neigbourIndex = i
        else:
            neigbourIndex = i+1
        newIndex = i / 2
        direction = "R"
    else:
        neigbourIndex = i-1
        newIndex = (i - 1) / 2
        direction = "L"

    node = direction + nodes[int(neigbourIndex)]
    return node, newIndex


def createUpperLevelNodes(nodes):
    upper_nodes = []
    for index in range(0, len(nodes), 2):
        if(index+1 >= len(nodes)):
            upper_node = nodes[index] + nodes[index]
        else:
            upper_node = nodes[index] + nodes[index+1]

        byte_upper_node = bytes.fromhex(upper_node)
        upper_nodes.append(sha1function(byte_upper_node))
    return upper_nodes


def getNeighbourPath(nodes, i):
    pathList = []
    start_level = math.ceil(math.log2(len(nodes)))
    for current_level in range(start_level, 0, -1):
        nodeInPath, i = findPathOnLevel(nodes, i)
        updatedNodes = createUpperLevelNodes(nodes)
        pathList.append(nodeInPath)
        nodes = updatedNodes
    return pathList


def getMerkleRoot(leaf, path):
    for i in range(0, len(path)):
        direction = path[i][0]
        neighbourLeaf = path[i][1:]

        if(direction == 'R'):
            upperLeaf = leaf + neighbourLeaf
        else:
            upperLeaf = neighbourLeaf + leaf

        newLeaf = bytes.fromhex(upperLeaf)
        leaf = sha1function(newLeaf)
    return leaf


with open("MerkleInfo.txt") as f:
    merkleInfo = f.read().splitlines()

i = int(merkleInfo[0])
j = int(merkleInfo[1])
nodes = merkleInfo[2:len(merkleInfo)]

merklePathForI = getNeighbourPath(nodes, i)
merkleRoot = getMerkleRoot(nodes[i], merklePathForI)
contatination = merklePathForI[len(merklePathForI)-j] + merkleRoot
print("Merkle path for i:", merklePathForI)
print()
print("MerkleRoot:", merkleRoot)
print()
print("Contatination:", contatination)
