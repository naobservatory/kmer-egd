from collections import defaultdict

def start():
    n_kmer_types_to_occurrences = defaultdict(int)
    with open("rothman.unenriched.counts") as inf:
        for line in inf:
            n_kmer_types, occurrences_of_each = line.strip().split()
            n_kmer_types = int(n_kmer_types)
            occurrences_of_each = int(occurrences_of_each)

            n_kmer_types_to_occurrences[occurrences_of_each] += n_kmer_types

    print("loaded")
                
    expanded.sort()

    print("sorted")
    
    total_occurrences = sum(n_kmer_types * occurrences_of_each
                            for occurrences_of_each, n_kmer_types
                            in n_kmer_types_to_occurrences.items())
    assert total_occurrences == sum(expanded)
    
    with open("rothman.unenriched.occurrences_by_type.cdf", "w") as outf:
        last_frac = -1
        last_occurrences = 0
        for type_index, occurrences in enumerate(expanded):
            frac = type_index / len(expanded)
            if frac - last_frac > 0.001 or occurrences/last_occurrences > 0.1:
                outf.write("%.1e\t%s%%\n" % (occurrences, frac*100))
                last_frac = frac
                last_occurrences = occurrences
        outf.write("%.1e\t%s%%\n" % (occurrences, frac*100))
    
if __name__ == "__main__":
    start()
