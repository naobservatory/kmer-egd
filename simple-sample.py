import random
import sys
import statsmodels.api as sm
import math
import numpy as np
from collections import defaultdict

# Simulate daily_reads over the specified number of days.
def start(days, daily_reads):
    days = int(days)
    daily_reads = int(daily_reads)

    rng = np.random.default_rng()
    days_arr_with_constant = sm.add_constant([[day] for day in range(days)])


    n_kmer_types_to_tokens = defaultdict(int)
    with open("rothman.unenriched.counts") as inf:
        for line in inf:
            n_kmer_types, tokens_of_each =\
                line.strip().split()
            n_kmer_types_to_tokens[int(tokens_of_each)] += int(
                n_kmer_types)

    total_tokens = sum(n_kmer_types * tokens_of_each
                       for tokens_of_each, n_kmer_types
                       in n_kmer_types_to_tokens.items())

    choices = []
    weights = []
    for tokens_of_each, n_kmer_types in \
        n_kmer_types_to_tokens.items():

        choices.append(tokens_of_each)
        weights.append(n_kmer_types)

    min_p = 1
    min_coef = None
    min_vals = []
    min_choice = None

    n_unique_kmers = sum(weights)

    block = 1000
    for i in range(int(n_unique_kmers/block)):
        for n, tokens_of_each in enumerate(random.choices(
                choices, weights, k=block)):

            probability = tokens_of_each/total_tokens

            if probability*daily_reads > 100:
                continue # speed things up; not going to identify exponential growth

            day_counts = rng.binomial(n=daily_reads, p=probability, size=days)
            if sum(day_counts) < 20:
                continue # speed things up; not going to identify exponential growth

            model = sm.GLM(day_counts, days_arr_with_constant,
                           family=sm.families.Poisson())
            result = model.fit()
            pvalue = result.pvalues[1]
            if pvalue < min_p:
                print("Found p=%.2e @simulation %.0f" % (
                    pvalue, i*block + n), flush=True)
                min_p = pvalue
                min_coef = result.params[1]
                min_vals = day_counts
                min_choice = tokens_of_each

    daily_growth = (math.exp(min_coef)-1)*100
    print("%.2e\t%.2f%%\t%s/%s\t%s" % (
        min_p, daily_growth, min_choice, total_tokens, "\t".join(
            str(x) for x in min_vals)))

if __name__ == "__main__":
    start(*sys.argv[1:])
