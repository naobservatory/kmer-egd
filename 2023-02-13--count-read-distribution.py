#!/usr/bin/env python3

import sys
import json
from collections import Counter
from Bio.SeqIO.QualityIO import FastqGeneralIterator

MAX_KMER_LEN=8

kmers = [Counter() for x in range(MAX_KMER_LEN)]

for (title, sequence, quality) in FastqGeneralIterator(sys.stdin):
    for k in range(1, MAX_KMER_LEN+1):
        for i in range(len(sequence) - k + 1):
            kmers[k-1][sequence[i:i+k]] += 1

print(json.dumps(kmers))
