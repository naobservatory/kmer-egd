import sys
from collections import Counter

spike_kmer_fname, = sys.argv[1:]

spike_kmers = {}
with open(spike_kmer_fname) as inf:
    for line in inf:
        kmer = line.strip()
        spike_kmers[kmer] = Counter()

for line in sys.stdin:
    for kmer in spike_kmers:
        if kmer in line:
            spike_kmers[kmer][hash(line)] += 1

for spike_kmer, counts in spike_kmers.items():
    print("%s\t%.0f\t%.0f" % (
        spike_kmer, sum(counts.values()), len(counts)))
