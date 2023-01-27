#!/usr/bin/env python3

import sys
from Bio.SeqIO.FastaIO import SimpleFastaParser
from Bio.SeqIO.QualityIO import FastqGeneralIterator

seq_fname, = sys.argv[1:]
K=40
to_match = set()

def rc(s):
    return "".join({'T':'A',
                    'G':'C',
                    'A':'T',
                    'C':'G',
                    'N':'N'}[x] for x in reversed(s))

if seq_fname.endswith(".fasta"):
    with open(seq_fname) as inf:
        (_, seq), = SimpleFastaParser(inf)
else:
    with open(seq_fname) as inf:
        seq, = inf

seq = seq.strip()
for i in range(len(seq) - K + 1):
    kmer_in = seq[i:i+K]
    for kmer in [kmer_in, rc(kmer_in)]:
        to_match.add(kmer)

for title, seq, quality in FastqGeneralIterator(sys.stdin):
    for i in range(len(seq) - K + 1):
        kmer = seq[i:i+K]
        if kmer in to_match:
            print(">%s\n%s" % (title, seq))
            # only extract the read once
            break
                
    
