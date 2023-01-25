#!/usr/bin/env python3

import sys
import glob
from Bio.SeqIO.FastaIO import SimpleFastaParser
from collections import Counter, defaultdict

iteration, contig = sys.argv[1:]

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

def get_base(vals):
    total = sum(vals.values())
    base, count = vals.most_common(1)[0]

    if count < 100 or count / total < 0.5:
        #print("Rejected: %s / %s = %.2f" % (count, total, count/total))
        return None

    return base

for loc, vals in sorted(next_vals.items()):
    base = get_base(vals)
    if not base:
        break
    
    new_contig[len(contig) + 1 + loc] = base

for loc, vals in sorted(prev_vals.items()):
    base = get_base(vals)
    if not base:
        break
        
    new_contig[-loc - 1] = base

new_contig = "".join(base for loc, base in sorted(new_contig.items()))
print(new_contig)

if new_contig == contig:
    sys.exit(42)
else:
    sys.exit(0)
                    
