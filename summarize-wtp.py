# How many k-mers were seen on at least N days?
# How many k-mers were seen at least N times on their M-most popular day?

import sys
import math
from collections import defaultdict

seen_n_days = defaultdict(int)
seen_nth_popular = defaultdict(lambda: defaultdict(int))

total = 0
for line in sys.stdin:
    total+=1

    line = line.strip()

    bucket, *vals = line.split('\t')
    vals = [int(x) for x in vals]

    n_nonzero = len(vals) - vals.count(0)

    seen_n_days[n_nonzero] += 1

    vals.sort()

    for i in range(len(vals)):
        pos = len(vals)-i-1
        val = vals[pos]
        if not val:
            continue
        seen_nth_popular[pos][int(math.log(val, 2))] += 1

print(total)
print()
for n_days, count in sorted(seen_n_days.items()):
    print("%s\t%s" % (n_days, count))
print()
for pos, d in sorted(seen_nth_popular.items()):
    for logval, count in sorted(d.items()):
        print("%s\t%s\t%s" % (
            pos, logval, count))
