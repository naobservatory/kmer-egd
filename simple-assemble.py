import sys

# Usage: cat *.reads | simple-assemble.py > foo.contigs

# Super simple greedy assembler, that should be enough for the cases we're
# handling.  We have some very high read counts for things that only showed up
# on a single day ("spikes") and we're trying to put them together into
# contigs.
from collections import defaultdict
from collections import Counter

next_vals = defaultdict(lambda: Counter()) # k-1 mer to following values
prev_vals = defaultdict(lambda: Counter()) # k-1 mer to preceeding values

K = 31
reads = []
counts = Counter()

for line in sys.stdin:
    read = line.strip()
    reads.append(read)

def to_kmers(read, k):
    for i in range(len(read) - k + 1):
        yield read[i:i+k]
    
for read in reads:
    for kmer in to_kmers(read, K):
        next_vals[kmer[:-1]][kmer[-1]] += 1
        prev_vals[kmer[1:]][kmer[0]] += 1
    for kmer in to_kmers(read, K-1):
        counts[kmer] += 1

while counts:
    contig, _ = counts.most_common()[0]
    #print("Starting\n- %s" % contig)

    while True:
        key = contig[:(K-1)]
        if key not in prev_vals:
            break
        base, _ = prev_vals[key].most_common()[0]
        del prev_vals[key]
        contig = base + contig
        #print("+ %s" % contig)

    while True:
        key = contig[-(K-1):]
        if key not in next_vals:
            break
        base, _ = next_vals[key].most_common()[0]
        del next_vals[key]
        contig = contig + base
        #print("+ %s" % contig)

    del counts[contig]

    if len(contig) > K + 10:
        print(contig)
