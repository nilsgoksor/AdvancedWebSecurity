import hashlib


def sha1function(nbr):
    hashf = hashlib.sha1()
    hashf.update(nbr)
    hash = hashf.hexdigest()
    return(hash)


hashfunction = hashlib.sha1()


with open("MerkleInfo.txt") as f:
    merkleInfo = f.read().splitlines()

leaf = merkleInfo[0]
path = merkleInfo[1:len(merkleInfo)]


for i in range(0, len(path)):
    direction = path[i][0]
    neighbourLeaf = path[i][1:]

    if(direction == 'R'):
        upperLeaf = leaf + neighbourLeaf
    else:
        upperLeaf = neighbourLeaf + leaf

    byteNode = bytes.fromhex(upperLeaf)
    leaf = sha1function(byteNode)

print("MERKLE ROOT", leaf)
