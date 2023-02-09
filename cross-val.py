import sys
import math
import statsmodels.api as sm
import gzip

import importlib
eval_buckets_sm = importlib.import_module("eval-buckets-sm")

def start(wtp, prefix, metadata):
    days = eval_buckets_sm.parse_metadata(wtp, metadata)
    kmers = set()

    with gzip.open("hc-%s-%s.poisson.gz" % (wtp, prefix), "rb") as inf:
        for line in inf:
            line = line.strip()
            if not line: continue

            _, _, _, _, kmer = line.split(b"\t")

            kmers.add(kmer.decode('utf-8'))

    print("Looking for %s kmers..." % len(kmers), file=sys.stderr)
    print()

    matching = 0
    for line in sys.stdin:
        line = line.strip()
        bucket, *vals = line.split('\t')

        if bucket not in kmers:
            continue

        matching += 1
        print("\r%.1f%%" % (matching/len(kmers)*100), file=sys.stderr, end="")

        vals = [int(x) for x in vals]

        if len(vals) != len(days):
            raise Exception("vals too short: got %s expected %s for %r" % (
                len(vals), len(days), line))

        pvalues = []
        first_day = None
        for i in range(10, len(vals)):
            result = eval_buckets_sm.eval_bucket(vals[:i+1], days[:i+1])
            if result:
                pvalue, _, _ = result
            elif not first_day:
                continue
            else:
                pvalue = 1

            pvalues.append(pvalue)
            if not first_day:
                first_day = i

        if not first_day:
            raise Exception("unable to evaluate %r" % line)

        if len(pvalues) == 1:
            continue # can't cross-validate if we only flagged the last day

        if pvalues[1] > pvalues[0]:
            # basic cross-val failed -- normally you'd expect to become more
            # confident with more data
            continue 

        print ("%s\t%s\t%s\t%s" % (
            bucket, first_day,
            ",".join("%.1e" % x for x in pvalues),
            "\t".join(str(x) for x in vals)))

if __name__ == "__main__":
    try:
        start(*sys.argv[1:])
    finally:
        print(file=sys.stderr)
        
