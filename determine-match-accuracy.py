#!/usr/bin/env python3

import sys
from Bio.SeqIO.FastaIO import SimpleFastaParser

seq_fname, = sys.argv[1:]
K=40
to_match = set()

def rc(s):
    return "".join({'T':'A',
                    'G':'C',
                    'A':'T',
                    'C':'G',
                    'N':'N'}[x] for x in reversed(s))

with open(seq_fname) as inf:
    seq, = inf
    seq = seq.strip()
    for i in range(len(seq) - K + 1):
        kmer_in = seq[i:i+K]
        for kmer in [kmer_in, rc(kmer_in)]:
            to_match.add(kmer)

for title, seq in SimpleFastaParser(sys.stdin):
    total = 0
    matches = 0
    for i in range(len(seq) - K + 1):
        kmer = seq[i:i+K]
        total += 1
        if kmer in to_match:
            matches += 1

    print ("%.2f\t%d\t%d" % (
        matches / total, matches, total))
    
                
    
