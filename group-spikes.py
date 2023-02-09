import sys
from Bio import Align

kmer_counts = {}
counted_kmers = []
for line in sys.stdin:
    count, kmer = line.strip().split("\t")
    counted_kmers.append((int(count), kmer))
    kmer_counts[kmer] = int(count)

counted_kmers.sort(reverse=True)

aligner = Align.PairwiseAligner()
# These are the scoring settings porechop uses by default.
# https://github.com/rrwick/Porechop/blob/master/porechop/porechop.py#L145
aligner.end_gap_score = 0
aligner.match_score = 3
aligner.mismatch_score = -6
aligner.internal_open_gap_score = -5
aligner.internal_extend_gap_score = -2

for count, kmer in counted_kmers:
    if kmer not in kmer_counts:
        continue # already clustered

    cluster = []
    for kmer2, kmer2_count in kmer_counts.items():
        alignment = aligner.align(kmer, kmer2)[0]
        if alignment.score > 110:
            count += kmer2_count
            cluster.append(kmer2)

    for kmer2 in cluster:
        del kmer_counts[kmer2]


    print("%s %s %s" % (count, len(cluster), cluster[0]))
    
