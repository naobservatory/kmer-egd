import sys
import math
from sklearn import linear_model

def start():
    clf = linear_model.PoissonRegressor()
    #sums = None
    days = None
    for line in sys.stdin:
        #if not sums:
        #    _, *sums = line.strip().split('\t')
        #    sums = [int(x) for x in sums]
        #    days = [[day] for day in range(len(sums))]
        #    continue

        bucket, *vals = line.strip().split('\t')
        vals = [int(x) for x in vals]

        if not days:
            days = [[day] for day in range(len(vals))]
        
        #print(repr(vals))
        
        # TODO: adjust by sums
        clf.fit(days, vals)
        print("%s\t%s\t%s" % (
            clf.coef_[0],
            clf.score(days, vals),
            bucket))


if __name__ == "__main__":
    start()
