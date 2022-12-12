#!/usr/bin/env python3

import sys
from Bio import Align

seq_fname, = sys.argv[1:]

K=28

to_match = set()

def rc(s):
    return "".join({'T':'A',
                    'G':'C',
                    'A':'T',
                    'C':'G',
                    'N':'N'}[x] for x in reversed(s))

with open(seq_fname) as inf:
    for line in inf:
        seq = line.strip()
        for i in range(len(seq) - K + 1):
            kmer_in = seq[i:i+K]
            for kmer in [kmer_in, rc(kmer_in)]:
                to_match.add(kmer)
        target = seq

aligner = Align.PairwiseAligner()
# These are the scoring settings porechop uses by default.
# https://github.com/rrwick/Porechop/blob/master/porechop/porechop.py#L145
aligner.end_gap_score = 0
aligner.match_score = 3
aligner.mismatch_score = -6
aligner.internal_open_gap_score = -5
aligner.internal_extend_gap_score = -2

def any_kmer_matches(s):
    for i in range(len(s) - K + 1):
        if s[i:i+K] in to_match:
            return True
    return False

for n, line in enumerate(sys.stdin):
    line = line.strip()
    if not any_kmer_matches(line):
        continue

    alignment_fwd = aligner.align(line, target)[0]
    alignment_rev = aligner.align(rc(line), target)[0]

    if alignment_fwd.score > alignment_rev.score:
        direction = 0
        alignment = alignment_fwd
    else:
        direction = 1
        alignment = alignment_rev

    if alignment.score / len(line) < 2.5:
        continue

    start = alignment.aligned[1][0][0]
    end = alignment.aligned[1][-1][-1]
    
    print("%.2f %s %s %s" % (alignment.score / len(line), direction, start, end))
    
    #if alignment.score / len(line) < 1:
    #    print("No match: %s" % line)
    #    print(alignment)


    #sys.stdout.write(line)
    
