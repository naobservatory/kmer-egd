import sys
import math
import statsmodels.api as sm

def start():
    days = None
    #for line in [
    #    "AAGAAGAGCAACAAGAAGAGCAACAAGAAGAGCAACAAGA "
    #    "0 0 0 0 0 0 0 0 5 5 0 1 5 7".replace(" ", "\t")]:

    if len(sys.argv) > 1:
        data = ["\t".join(sys.argv[1:])]
    else:
        data = sys.stdin
    
    for line in data:
        line = line.strip()
        
        bucket, *vals = line.split('\t')
        vals = [int(x) for x in vals]

        # Not worth running regression if we have too little data
        if sum(vals) < 20:
            continue

        if not days:
            days = [[day] for day in range(len(vals))]

        model = sm.GLM(vals, sm.add_constant(days),
                       family=sm.families.Poisson())
        result = model.fit()
        pvalue = result.pvalues[1]
        coef = result.params[1]
        ci_025, ci_975 = result.conf_int()[1]

        # These are in log space; convert to percentage daily growth.
        coef = math.exp(coef)-1
        ci_025 = math.exp(ci_025)-1
        ci_975 = math.exp(ci_975)-1
        ci_width = ci_975 - ci_025

        # Skip things that are decreasing
        if coef < 0:
            continue
        
        #print("%.2E\t%.3f\t%.3f\t%.3f\t%s" % (
        #    pvalue,
        #    coef,
        #    ci_025,
        #    ci_width,
        #    line))

        print("%s\t%.1f%%\t%.1f%%\t%.2E\t%.3f" % (
            " ".join(str(x) for x in vals),
            coef*100,
            ci_025*100,
            pvalue,
            coef/ci_width))

        if len(sys.argv) > 1:
            import code
            code.interact(local=locals())

if __name__ == "__main__":
    start()
