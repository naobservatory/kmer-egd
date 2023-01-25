#!/usr/bin/env python3

import sys
from collections import Counter, defaultdict
from Bio.SeqIO.FastaIO import SimpleFastaParser

K=40

targets = sys.argv[1:]

# target -> best kmer
best_kmers = {}
# target -> best kmer count
best_kmer_counts = Counter()

def rc(s):
    return "".join({'T':'A',
                    'G':'C',
                    'A':'T',
                    'C':'G',
                    'N':'N'}[x] for x in reversed(s))

# target -> kmers
target_kmers = {}

# kmer -> target
kmers_target = {}

for target in targets:
    with open(target) as inf:
        (title, seq), = SimpleFastaParser(inf)

        target_kmers[target] = set(
            seq[i:i+K] for i in range(len(seq) - K + 1))

dups = set()
for target, kmers in target_kmers.items():
    for kmer in kmers:
        if kmer in kmers_target:
            dups.add(kmer)
        kmers_target[kmer] = target

for kmer in dups:
    del kmers_target[kmer]

for line in sys.stdin:
    kmer, *counts = line.strip().split("\t")
    if kmer in kmers_target:
        target = kmers_target[kmer]
        kmer_total = sum(int(x) for x in counts)
        if kmer_total > best_kmer_counts[target]:
            best_kmer_counts[target] = kmer_total
            best_kmers[target] = kmer

for target in sorted(targets):
    print (target, best_kmer_counts[target], best_kmers.get(target, ''))

                
    
        
