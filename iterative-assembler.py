#!/usr/bin/env python3

import sys
import glob
from Bio.SeqIO.FastaIO import SimpleFastaParser
from collections import Counter, defaultdict

iteration, contig, seed_count = sys.argv[1:]

# seed_count is how prevalant the seed is in the data, and we use it to tune
# our thresholds.
seed_count = int(seed_count)

# position relative to start of contig -> ACGT -> count
# 0 = one before contig
# 1 = two before contig
prev_vals = defaultdict(Counter)
# position relative to end of contig -> ACGT -> count
# 0 = one after contig
# 1 = two after contig
next_vals = defaultdict(Counter)

K=40

start = contig[:K]
end = contig[-K:]

for fname in glob.glob("*.%s.fasta" % iteration):
    with open(fname) as inf:
        for title, seq in SimpleFastaParser(inf):
            if start in seq:
                start_pos = seq.index(start) - 1
                for i in range(start_pos):
                    prev_vals[i][seq[start_pos - i]] += 1
            if end in seq:
                end_pos = seq.index(end) + K
                for i in range(len(seq)-end_pos):
                    next_vals[i][seq[end_pos + i]] += 1

new_contig = {}
for loc, base in enumerate(contig):
    new_contig[loc] = base

def get_base(vals, max_count):
    total = sum(vals.values())
    base, count = vals.most_common(1)[0]

    # These rules could be a lot fancier.  The basic principle is that we'd get
    # the most accuracy by adding only the single most confident base each
    # time, but if we did this we'd need a very large number of iterations.
    # But if we're confident enough about the bases we're adding, though, we
    # can add dozens in a single iteration, making it *much* faster.
    #
    # The main idea is that once half the reads have dropped off we should
    # rescan, and we should rescan earlier than that for tricky calls.
    if (count < 5 or
        count < max_count/2 or (
            count < 0.85*max_count and count / total < 0.5)):
        sys.stderr.write("Rejected (max_count=%s): %s / %s = %.2f\n" % (
            max_count, count, total, count/total))
        return None
    
    return base

if 0 in next_vals:
    max_next = sum(next_vals[0].values())
    for loc, vals in sorted(next_vals.items()):
        base = get_base(vals, max_next)
        if not base:
            break
        new_contig[len(contig) + 1 + loc] = base

if 0 in prev_vals:
    max_prev = sum(prev_vals[0].values())
    for loc, vals in sorted(prev_vals.items()):
        base = get_base(vals, max_prev)
        if not base:
            break
        new_contig[-loc - 1] = base

new_contig_str = "".join(base for loc, base in sorted(new_contig.items()))
            
print(new_contig_str)

if new_contig_str == contig:
    sys.exit(42)
else:
    sys.exit(0)
                    
