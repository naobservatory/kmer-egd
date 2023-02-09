#!/usr/bin/env python3

import sys
from Bio import Align

seq_fname, = sys.argv[1:]

K=28

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
                to_match.add(kmer)
        target = seq

def any_kmer_matches(s):
    return False

def process(line):
    for i in range(len(line) - K + 1):
        if line[i:i+K] in to_match:
            print(line)
            return

for line in sys.stdin:
    line = line.strip()
    process(line)

