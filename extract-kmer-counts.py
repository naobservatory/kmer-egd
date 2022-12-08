#!/usr/bin/env python3

import sys
prefix, seq_fname = sys.argv[1:]

K=40

to_match = set()

with open(seq_fname) as inf:
    for line in inf:
        seq = line.strip()
        for i in range(len(seq) - K + 1):
            kmer = seq[i:i+K]
            if kmer.startswith(prefix):
                to_match.add(kmer)

for line in sys.stdin:
    if line.split()[0] in to_match:
        sys.stdout.write(line)
    
