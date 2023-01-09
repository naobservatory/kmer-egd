#!/usr/bin/env python3

import sys
import math

for line in sys.stdin:
    vals = line.strip().split()[1:]
    vals = [int(x) for x in vals]
    n_vals = len(vals)

    mean = sum(vals) / n_vals
    squared_errors = [(x - mean)*(x-mean) for x in vals]
    rms_error = math.sqrt(sum(squared_errors) / n_vals)

    print("%.2f\t%.2f\t%.2f" % (
        mean, rms_error, rms_error / mean))
