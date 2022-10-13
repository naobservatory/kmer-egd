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
    
def run(days, daily_reads, growth, last_day_prevalance, simulations):
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
    return median

def determine_scalar(growth):
    # If we want to catch something when 1 in 100 people have been cumulatively
    # infected, we need to use the growth rate adjust last_day_prevalance.
    population = 3e6
    daily_new_infections = 1
    cumulative_infections = 1
    for day in range(1,10000):
        daily_new_infections *= growth
        cumulative_infections += daily_new_infections
        if cumulative_infections / population >= 0.01:
            break
    daily_new_infection_rate = daily_new_infections / population
   
    #print("Scaled by assuming an infection rate of "
    #      "%.2f%%, which meant by %.3f" % (
    #          daily_new_infection_rate*100, daily_new_infection_rate / 0.001))

    # last_day_prevalance is assuming a daily rate of 0.001
    return daily_new_infection_rate / 0.001

# ex: days=60 daily_reads=7e9 growth=0.1 last_day_prevalance=8e-10
#     simulations=100
#
# The input of last_day_prevalance is the number of reads we would expect to
# see at a new daily infection rate of 100 per 100k.
def start(days, daily_reads, growth, last_day_prevalance, simulations):
    days = int(days)
    daily_reads = float(daily_reads)
    growth = 1+float(growth)
    last_day_prevalance = float(last_day_prevalance)
    simulations = int(simulations)

    # last_day_prevalance is assuming a daily rate of 0.001
    last_day_prevalance *= determine_scalar(growth)
    
    print("%.1e" % run(
        days, daily_reads, growth, last_day_prevalance, simulations))

if __name__ == "__main__":
    start(*sys.argv[1:])
