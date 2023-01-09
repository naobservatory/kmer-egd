#!/usr/bin/env python3

import sys
import math
from collections import Counter

counts = Counter()

for line in sys.stdin:
    vals = line.strip().split()[1:]
    vals = [int(x) for x in vals]
    n_vals = len(vals)

    mean = sum(vals) / n_vals
    squared_errors = [(x - mean)*(x-mean) for x in vals]
    rms_error = math.sqrt(sum(squared_errors) / n_vals)

    log_mean = math.log(mean, 10)
    counts["%.2f\t%.2f" % (log_mean, rms_error / mean)] += 1

for record, count in counts.items():
    print("%s\t%s" % (count, record))
