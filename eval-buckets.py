import sys
import math
from sklearn import linear_model

def start():
    clf = linear_model.PoissonRegressor()
    #sums = None
    days = None
    for line in sys.stdin:
        line = line.strip()
        
        #if not sums:
        #    _, *sums = line.split('\t')
        #    sums = [int(x) for x in sums]
        #    days = [[day] for day in range(len(sums))]
        #    continue

        bucket, *vals = line.split('\t')
        vals = [int(x) for x in vals]

        # Not worth running regression if we have too little data
        if sum(vals) < 20:
            continue

        if not days:
            days = [[day] for day in range(len(vals))]

        #print(repr(vals))

        # TODO: adjust by sums
        clf.fit(days, vals)
        print("%.5f\t%.5f\t%s" % (
            clf.coef_[0],
            clf.score(days, vals),
            line))


if __name__ == "__main__":
    start()
