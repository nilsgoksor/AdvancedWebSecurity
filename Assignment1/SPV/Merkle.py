import hashlib


def sha1function(byte_vector):
    sha1 = hashlib.sha1()
    sha1.update(byte_vector)
    return sha1.hexdigest()


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

leaf = merkleInfo[0]
path = merkleInfo[1:len(merkleInfo)]

merkleRoot = getMerkleRoot(leaf, path)

print("MERKLE ROOT;", merkleRoot)
