#!/usr/bin/env python3
import sys
from collections import Counter

counts = Counter()
for line in sys.stdin:
    count, record = line.strip().split('\t', 1)
    counts[record] += int(count)

for record, count in counts.items():
    print("%s\t%s" % (count, record))
    
