#!/usr/bin/env python3

import sys
import glob
from Bio.SeqIO.FastaIO import SimpleFastaParser
from collections import Counter, defaultdict

target, = sys.argv[1:]
iteration = max(int(fname.split("/")[-1].split(".")[0])
                for fname in glob.glob("%s/*.contig.seq" % target))

K=40
END_LENGTH=100

with open("%s/%s.contig.seq" % (target, 0)) as inf:
    seed = inf.read().strip()

with open("%s/%s.contig.seq" % (target, iteration)) as inf:
    prev_contig = inf.read().strip()
    prev_start = prev_contig[:K]
    prev_end = prev_contig[-K:]

seed_count = 0
prev_start_count = 0
prev_end_count = 0

seqs = []
for fname in glob.glob("%s/*.%s.fasta" % (target, iteration)):
    with open(fname) as inf:
        for title, seq in SimpleFastaParser(inf):
            seqs.append(seq)
            if seed in seq:
                seed_count += 1
            if prev_start in seq:
                prev_start_count += 1
            if prev_end in seq:
                prev_end_count += 1

def get_base(vals):
    total = sum(vals.values())
    if not total:
        return None
    base, count = vals.most_common(1)[0]

    # These rules could be a lot fancier.  The basic principle is that we'd get
    # the most accuracy by adding only the single most confident base each
    # time, but if we did this we'd need a very large number of iterations.
    # But if we're confident enough about the bases we're adding, though, we
    # can add dozens in a single iteration, making it *much* faster.
    #
    # The main idea is that once enough reads have dropped off we should
    # rescan.
    if (count < 10 or
        count < seed_count / 1000 or
        count < max(prev_start_count, prev_end_count) / 100):

        sys.stderr.write(
            "%s rejected (seed_count=%s, max(%s, %s)): %s / %s = %.2f\n" % (
                target, seed_count, prev_start_count, prev_end_count,
                count, total, count/total))
        return None

    return base

# Each time through the loop we look at every read, and if it matches either
# the start or end of the contig we count the distribution of bases.  We take
# the most common base, and keep going.
contig = prev_contig[END_LENGTH:-END_LENGTH]
if len(contig) < len(seed):
    contig = seed

need_next = True
need_prev = True
while need_next or need_prev:
    start = contig[:K]
    end = contig[-K:]

    next_bases = Counter()
    prev_bases = Counter()

    for seq in seqs:
        if need_prev:
            if start in seq:
                start_pos = seq.index(start) - 1
                if start_pos >= 0:
                    prev_bases[seq[start_pos]] += 1
        if need_next:
            if end in seq:
                end_pos = seq.index(end) + K
                if end_pos < len(seq):
                    next_bases[seq[end_pos]] += 1

    if need_next:
        next_base = get_base(next_bases)
        if next_base:
            contig = contig + next_base
        else:
            need_next = False
    if need_prev:
        prev_base = get_base(prev_bases)
        if prev_base:
            contig = prev_base + contig
        else:
            need_prev = False

if contig == prev_contig:
    out_prefix = "final_contig"
else:
    out_prefix = "%s.contig" % (iteration + 1)

with open("%s/%s.seq" % (target, out_prefix), "w") as outf:
    outf.write("%s\n" % contig)
