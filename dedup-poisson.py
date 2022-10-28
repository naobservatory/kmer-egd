import sys

best_p_value_per_kmer = {}
best_days_per_kmer = {}
for line in sys.stdin:
    p_value, _, _, days, kmer = line.strip().split("\t")

    p_value = float(p_value)
    days = int(days)
    
    if (kmer not in best_p_value_per_kmer or
        p_value < best_p_value_per_kmer[kmer]):
        
        best_p_value_per_kmer[kmer] = p_value
        best_days_per_kmer[kmer] = days

records = []
for kmer, p_value in best_p_value_per_kmer.items():
    records.append((p_value, best_days_per_kmer[kmer], kmer))

records.sort()
    
for p_value, days, kmer in records:
    print("%.5e\t%s\t%s" % (p_value, days, kmer))

    
