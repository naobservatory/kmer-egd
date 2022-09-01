import sys
import json
from collections import defaultdict

# input: fastq file
# output:
#   one line per position in input, in order
#   {'F': count of F, ':': count of :, etc}

counts=[]
for i in range(151):
    counts.append(defaultdict(int))

for line in sys.stdin:
    line = line.strip()
    if 'FF' in line:
        for i, c in enumerate(line):
            if i < len(counts):
                counts[i][c] += 1

for count in counts:
    print(json.dumps(count))
