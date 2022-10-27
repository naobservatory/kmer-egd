import sys
import math
import statsmodels.api as sm
import dateutil.parser

def too_little_data(vals):
    # Not worth running regression if we have too little data.  Need to see
    # at least five instances, and at least three times total.
    return sum(vals) < 5 or vals.count(0) > len(vals)-3

def parse_metadata(wtp, metadata):
    first_date = None

    days = []

    # file is sorted by days already
    with open(metadata) as inf:
        for line in inf:
            fname, date, line_wtp, is_enriched = line.strip().split("\t")

            # Metadata has both forward and reverse reads, but we just care
            # about sample dates so ignore reverse reads
            if not fname.endswith("_1.fastq.gz"): continue

            # only looking at the specified wtp
            if line_wtp != wtp: continue

            # only considering unenriched data
            if is_enriched != "0": continue

            date = dateutil.parser.isoparse(date)

            if first_date is None:
                first_date = date

            days.append([(date - first_date).days])

    return days

def start(wtp, metadata):
    days = parse_metadata(wtp, metadata)

    for line in sys.stdin:
        line = line.strip()

        if not line: continue

        bucket, *vals = line.split('\t')
        vals = [int(x) for x in vals]

        if len(vals) != len(days):
            raise Exception("vals too short: got %s expected %s for %r" % (
                len(vals), len(days), line))

        if too_little_data(vals):
            continue

        for i in range(10, len(vals)):
            eval_bucket(vals[:i+1], days[:i+1], bucket)

def eval_bucket(vals, days, bucket):
    if too_little_data(vals):
        return

    model = sm.GLM(vals, sm.add_constant(days),
                   family=sm.families.Poisson())
    try:
        result = model.fit()
    except ValueError:
        print("ERROR\t%s" % bucket)
        return

    pvalue = result.pvalues[1]

    if pvalue > 1e-5:
        # Rough filtering to exclude most uninteresting output
        return

    coef = result.params[1]
    ci_025, ci_975 = result.conf_int()[1]

    # These are in log space; convert to percentage daily growth.
    coef = math.exp(coef)-1
    ci_025 = math.exp(ci_025)-1

    print("%.4e\t%.1f%%\t%.1f%%\t%s\t%s" % (
        pvalue,
        coef*100,
        ci_025*100,
        len(vals),
        bucket))

if __name__ == "__main__":
    start(*sys.argv[1:])
