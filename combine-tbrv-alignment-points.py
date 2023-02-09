#!/usr/bin/env python3

import glob
from collections import Counter

fwd_starts = Counter()
rev_starts = Counter()

for fname in glob.glob("SRR*.tbrv.alignment-points"):
    with open(fname) as inf:
        for line in inf:
            score, direction, start, end = line.strip().split()
            if direction == "0":
                fwd_starts[int(start)] += 1
            else:
                rev_starts[int(end)] += 1

max_pos = max(max(fwd_starts), max(rev_starts))
                
with open("tbrv.summary", "w") as outf:
    for pos in range(max_pos + 1):
        outf.write("%s\t%s\t%s\n" % (pos, fwd_starts[pos], rev_starts[pos]))
