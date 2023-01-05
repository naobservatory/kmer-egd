#!/usr/bin/env python3

import sys
from collections import defaultdict

wtp_counts = defaultdict(list)
for line in sys.stdin:
    accession, date, wtp, length = line.strip().split()
    length = int(length)
    if length >= 150:
        wtp_counts[wtp].append((date, accession))

for wtp, counts in sorted(wtp_counts.items()):
    if len(counts) > 7:
        for date, accession in sorted(counts):
            print ("%s\t%s\t%s" % (
                accession, date, wtp))
