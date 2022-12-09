#!/usr/bin/env python3

import sys
prefix, seq_fname = sys.argv[1:]

K=40

to_match = set()

def rc(s):
    return "".join({'T':'A',
                    'G':'C',
                    'A':'T',
                    'C':'G',
                    'N':'N'}[x] for x in reversed(s))

with open(seq_fname) as inf:
    for line in inf:
        seq = line.strip()
        for i in range(len(seq) - K + 1):
            kmer_in = seq[i:i+K]
            for kmer in [kmer_in, rc(kmer_in)]:
                if kmer.startswith(prefix):
                    to_match.add(kmer)

for line in sys.stdin:
    if line.split()[0] in to_match:
        sys.stdout.write(line)
    
