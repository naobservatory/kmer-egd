import sys
import math
import statsmodels.api as sm

def too_little_data(vals):
    # Not worth running regression if we have too little data.  Need to see
    # at least 10 instances, and at least four times total.
    return sum(vals) < 5 or vals.count(0) > len(vals)-3

def start():
    days = None
    printed = False
    for line in sys.stdin:
        line = line.strip()

        bucket, *vals = line.split('\t')
        vals = [int(x) for x in vals]
        if not days:
            days = [[day] for day in range(len(vals))]

        if too_little_data(vals):
            continue

        for i in range(10, len(vals)):
            printed = printed or eval_bucket(vals[:i+1], days[:i+1], bucket)

    if not printed:
        print("1 found nothing")

def eval_bucket(vals, days, bucket):
    if too_little_data(vals):
        return False

    model = sm.GLM(vals, sm.add_constant(days),
                   family=sm.families.Poisson())
    result = model.fit()
    pvalue = result.pvalues[1]

    if pvalue > 1e-5:
        # Rough filtering to exclude most uninteresting output
        return False

    coef = result.params[1]
    ci_025, ci_975 = result.conf_int()[1]

    # These are in log space; convert to percentage daily growth.
    coef = math.exp(coef)-1
    ci_025 = math.exp(ci_025)-1
    ci_975 = math.exp(ci_975)-1
    ci_width = ci_975 - ci_025

    print("%.4e\t%.1f%%\t%.1f%%\t%.3f\t%s\t%s" % (
        pvalue,
        coef*100,
        ci_025*100,
        coef/ci_width,
        len(vals),
        bucket))

    return True

if __name__ == "__main__":
    start()
