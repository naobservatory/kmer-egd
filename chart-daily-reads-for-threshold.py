import sys

import importlib
simulate_one_kmer = importlib.import_module("simulate-one-kmer")

def start(threshold, last_day_prevalance):
    threshold = float(threshold)
    last_day_prevalance = float(last_day_prevalance)

    for int_growth in range(1,30):
        growth =  1 + int_growth/100

        adjusted_last_day_prevalance = last_day_prevalance * \
            simulate_one_kmer.determine_scalar(growth)

        def get_pvalue(daily_reads):
            return simulate_one_kmer.run(
                days=180,
                daily_reads=daily_reads,
                growth=growth,
                last_day_prevalance=adjusted_last_day_prevalance,
                simulations=100)
        
        lower_daily_reads = 1e8
        upper_daily_reads = 1e18
 
        if (threshold < get_pvalue(upper_daily_reads) or
            threshold > get_pvalue(lower_daily_reads)):
            raise Exception("bad initial conditions at %s" % (
                int_growth))

        while True:
            guess_daily_reads = (
                upper_daily_reads - lower_daily_reads) / 2 + lower_daily_reads
            p_value = get_pvalue(guess_daily_reads)

            if p_value < threshold:
                upper_daily_reads = guess_daily_reads
            else:
                lower_daily_reads = guess_daily_reads
                
            #print("[%.2e, %.2e] %.2e" % (
            #    lower_daily_reads, upper_daily_reads, p_value))
            
            if abs((upper_daily_reads - lower_daily_reads) /
                   lower_daily_reads) < .01:
                # our two bounds are within 1%, good enough
                break

        print("%.2f%%\t%.2e" % ((growth-1)*100,
                                (lower_daily_reads + upper_daily_reads)/2))
        #print("%.2e" % ((lower_daily_reads + upper_daily_reads)/2))

if __name__ == "__main__":
    start(*sys.argv[1:])
        
