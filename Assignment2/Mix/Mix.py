from pcapfile import savefile

def getBatchesPhase(NazirIP, MixIp, ipPackages):
    newBatch = set()
    allBatches = []
    fromNazir = False
    lastPackage = ipPackages[0]

    for i in range(len(ipPackages)):
        src = ipPackages[i]["src"]
        dst = ipPackages[i]["dst"]

        batchComplete = False
        if i < len(ipPackages)-1:
            nextPackageSrc = ipPackages[i+1]["src"]
            if nextPackageSrc != MixIp:
                batchComplete = True
        
        if lastPackage["src"] == NazirIP:
            fromNazir = True
        
        if fromNazir and src == MixIp:
            newBatch.add(dst)

            if batchComplete:
                allBatches.append(newBatch)
                newBatch = set()
                fromNazir = False
            
        lastPackage = ipPackages[i]

    return allBatches


def learningPhase(allBatches, amountOfPartners):
    disjunktBatches = []

    while(len(disjunktBatches)<amountOfPartners):
        for batch in allBatches:
            batchIsDisjunkt = True

            for disjunktBatch in disjunktBatches:
                if batch & disjunktBatch != set():
                    batchIsDisjunkt = False

            if batchIsDisjunkt:
                disjunktBatches.append(batch)
                allBatches.remove(batch)

    return disjunktBatches

def excludingPhase(allBatches, disjunktBatches):
    for batch in allBatches:
        matchingBatches = []
        
        for disjunktBatch in disjunktBatches:
            if batch & disjunktBatch != set():
                matchingBatches.append(disjunktBatch)

        if len(matchingBatches) == 1:
            matchingBatch = matchingBatches[0]
            disjunktBatches.remove(matchingBatch)
            match = matchingBatch & batch
            disjunktBatches.append(match)
    
    sum = 0
    for disjunktBatch in disjunktBatches:
        ipString = list(disjunktBatch)[0].split(".")
        fullHexString = ''
        for ipNbr in ipString:
            fullHexString = fullHexString + hex(int(ipNbr))[2:].zfill(2)
        value = int(fullHexString,16)
        sum = sum + value
    return sum

def main():
    NazirIP = '61.152.13.37'
    MixIP = '95.235.155.122'
    amountOfPartners = 8
    
    testcap = open('cia.log.3.pcap', 'rb')
    capfile = savefile.load_savefile(testcap, layers=2, verbose=True)
    
    ipPackages = []
    for pkt in capfile.packets:
        timestamp = pkt.timestamp    
        #eth_src = pkt.packet.src.decode('UTF8')
        #eth_dst = pkt.packet.dst.decode('UTF8')
        ip_src = pkt.packet.payload.src.decode('UTF8')
        ip_dst = pkt.packet.payload.dst.decode('UTF8')

        ipPackages.append({
            "src": ip_src,
            "dst": ip_dst
        })

    allBatches = getBatchesPhase(NazirIP, MixIP, ipPackages)
    disjunktBatches = learningPhase(allBatches, amountOfPartners)
    answer = excludingPhase(allBatches, disjunktBatches)
    print(answer)
    
print("Answer:")
main()