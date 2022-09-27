import random
import sys
import statsmodels.api as sm
import math
import numpy as np

days, daily_reads, simulations = sys.argv[1:]
days = int(days)
daily_reads = int(daily_reads)
simulations = int(simulations)

choices = []
weights = []
with open("tmp.counts.AA.uniqd") as inf:
    for line in inf:
        number_of_type_occurring_this_often, occurences_per_type = \
            line.strip().split()
        occurences_per_type = int(occurences_per_type)
        number_of_type_occurring_this_often = int(
            number_of_type_occurring_this_often)

        choices.append(occurences_per_type)
        weights.append(number_of_type_occurring_this_often)
total = sum(weights)

rng = np.random.default_rng()

days_arr_with_constant = sm.add_constant([[day] for day in range(days)])

min_p = 1
min_coef = None
min_vals = []
min_choice = None
for choice in random.choices(choices, weights, k=simulations):
    day_counts = rng.binomial(n=daily_reads, p=choice/total, size=days)
    if sum(day_counts) < 20:
        continue
        
    model = sm.GLM(day_counts, days_arr_with_constant,
                   family=sm.families.Poisson())
    result = model.fit()
    pvalue = result.pvalues[1]
    if pvalue < min_p:
        min_p = pvalue
        min_coef = result.params[1]
        min_vals = day_counts
        min_choice = choice
        
daily_growth = (math.exp(min_coef)-1)*100
print("%.2e\t%.2f%%\t%s/%s\t%s" % (
    min_p, daily_growth, min_choice, total, "\t".join(
        str(x) for x in min_vals)))
    
