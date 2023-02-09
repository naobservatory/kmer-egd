import sys
from collections import defaultdict, Counter

K=17

def start(seed):
    prv = defaultdict(Counter)
    nxt = defaultdict(Counter)
    
    for line in sys.stdin:
        line = line.strip()
        for i in range(1, len(line) - K):
            kmer = line[i:i+K]
            prv[kmer][line[i-1]] += 1
            nxt[kmer][line[i+K]] += 1

    contig = seed
    while True:
        kmer = contig[:K]
        if kmer not in prv: break
        (base, count), = prv[kmer].most_common(1)
        contig = base + contig
        del prv[kmer]

    while True:
        kmer = contig[-K:]
        if kmer not in nxt: break
        (base, count), = nxt[kmer].most_common(1)
        contig = contig + base
        del nxt[kmer]

    print(contig)        

if __name__ == "__main__":
    start(*sys.argv[1:])

