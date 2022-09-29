import sys
import numpy as np
import statsmodels.api as sm
import math

rng = np.random.default_rng()

def simulate(daily_reads, daily_probabilities, days_arr_with_constant):
    day_counts = rng.binomial(n=daily_reads, p=daily_probabilities,
                              size=len(daily_probabilities))
    if sum(day_counts) < 5:
        return 1  # can't possibly detect exponential growth

    return sm.GLM(day_counts, days_arr_with_constant,
                  family=sm.families.Poisson()).fit().pvalues[1]
    
# ex: days=14 daily_reads=122000000 growth=0.1 last_day_prevalance=1e-13
#     simulations=1000
def start(days, daily_reads, growth, last_day_prevalance, simulations):
    days = int(days)
    daily_reads = float(daily_reads)
    growth = 1+float(growth)
    last_day_prevalance = float(last_day_prevalance)
    simulations = int(simulations)

    days_arr_with_constant = sm.add_constant([[day] for day in range(days)])
    
    daily_probabilities = []
    cur_prevalance = last_day_prevalance
    for _ in range(days):
        daily_probabilities.append(cur_prevalance)
        cur_prevalance /= growth
    daily_probabilities.reverse()

    pvalues = [
        simulate(daily_reads, daily_probabilities, days_arr_with_constant)
        for _ in range(simulations)]
    pvalues.sort()
    median = pvalues[len(pvalues)//2]
    print("%.1e" % median)
        
if __name__ == "__main__":
    start(*sys.argv[1:])
