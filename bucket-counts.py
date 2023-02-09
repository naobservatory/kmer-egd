import sys
import math
from collections import defaultdict
histogram = defaultdict(int)
coverage = defaultdict(int)

all_count = 0

for line in sys.stdin:
    val, count = line.strip().split()
    val = int(val)
    count = int(count)

    bucket = int(math.log(val, 2))

    histogram[bucket] += count
    coverage[bucket] += (count * val)

    all_count += count * val

for bucket, count in sorted(histogram.items()):
    print("[%s-%s)\t%s\t%s" % (2**bucket, 2**(bucket+1), count, coverage[bucket]))


print(all_count)
