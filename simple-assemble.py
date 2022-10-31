import sys

# Usage: cat hc-HTP-*.spikes.NN | simple-assemble.py > hc-HTP.spike-contigs.NN

# Super simple greedy assembler, that should be enough for the cases we're
# handling.  We have some very high read counts for things that only showed up
# on a single day ("spikes") and we're trying to put them together into
# contigs.

next_vals = {} # k-1 mer to following value
prev_vals = {} # k-1 mer to preceeding value

kmer_counts = []
for line in sys.stdin:
    count, kmer = line.strip().split("\t")
    kmer_counts.append((int(count), kmer))
    if not K:
        K = len(kmer)

kmer_counts.sort(reverse=True)

# because kmer_counts is sorted in descending order, this breaks ties by
# frequency
for count, kmer in kmer_counts:
    head = kmer[:-1]
    if head not in next_vals:
        next_vals[head] = kmer[-1]

    tail = kmer[1:]
    if tail not in prev_vals:
        prev_vals[tail] = kmer[0]

while kmer_counts:
    count, contig = kmer_counts.pop(0)

    while True:
        key = contig[:(K-1)]
        if key not in prev_vals:
            break
        contig = prev_vals[key] + contig
        del prev_vals[key]
    
    while True:
        key = contig[-(K-1):]
        if key not in next_vals:
            break
        contig = contig + next_vals[key]
        del next_vals[key]
        
    print("%s\t%s" % (count, contig))
