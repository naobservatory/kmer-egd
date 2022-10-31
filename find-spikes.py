import sys

THRESHOLD = 100

for line in sys.stdin:
    line = line.strip()

    if not line: continue

    bucket, *vals = line.split('\t')
    vals = [int(x) for x in vals]
    vals.sort()

    # If the largest value is at least 100x the second largest, that's very
    # surprising under both the simple model of "everything is about constant"
    # and a more complex model of "everything is exponential with some not that
    # big growth/decay rate".  These should be good to look into from a
    # perspective of understanding sequencing noise.
    if vals[-1] > (vals[-2]+1) * THRESHOLD:
        print("%s\t%s" % (vals[-1], line))
