#!/usr/bin/env python3

import sys
from Bio.SeqIO.QualityIO import FastqGeneralIterator

accession, contig = sys.argv[1:]
K=40

def rc(s):
    return "".join({'T':'A',
                    'G':'C',
                    'A':'T',
                    'C':'G',
                    'N':'N'}[x] for x in reversed(s))

start = contig[:K]
end = contig[-K:]

start_rc = rc(start)
end_rc = rc(end)

for title, seq, quality in FastqGeneralIterator(sys.stdin):
    if start in seq or end in seq:
        print(">%s\n%s" % (title, seq))
    elif start_rc in seq or end_rc in seq:
        print(">%s:rc\n%s" % (title, rc(seq)))
        
                
    
