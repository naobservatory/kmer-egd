#!/usr/bin/env python3

import glob
from collections import Counter

# target -> best kmer
best_kmers = {}
# target -> best kmer count
best_kmer_counts = Counter()

for fname in glob.glob("best-seeds.*.tmp"):
    with open(fname) as inf:
        for line in inf:
            target, count, kmer = line.strip().split()
            count = int(count)
            if count > best_kmer_counts[target]:
                best_kmer_counts[target] = count
                best_kmers[target] = kmer


for target in sorted(best_kmers):
    print (target, best_kmer_counts[target], best_kmers[target])

