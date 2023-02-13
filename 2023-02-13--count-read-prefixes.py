#!/usr/bin/env python3

import sys
import json
from collections import Counter
from Bio.SeqIO.QualityIO import FastqGeneralIterator

MAX_PREFIX_LEN=8

prefixes = [Counter() for x in range(MAX_PREFIX_LEN)]

for (title, sequence, quality) in FastqGeneralIterator(sys.stdin):
    for i in range(MAX_PREFIX_LEN):
        if len(sequence) < i + 1:
            break
        prefixes[i][sequence[:i+1]] += 1

print(json.dumps(prefixes))
