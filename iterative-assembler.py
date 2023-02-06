#!/usr/bin/env python3

import os
import sys
import glob
import subprocess
from collections import Counter, defaultdict
from Bio.SeqIO.FastaIO import SimpleFastaParser

thisdir = os.path.dirname(os.path.realpath(__file__))
iterative_assembler_exe = os.path.join(thisdir, "iterative-assembler")

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

prev_start_count = 0
prev_end_count = 0

seqs = []
for fname in glob.glob("%s/*.%s.fasta" % (target, iteration)):
    with open(fname) as inf:
        for title, seq in SimpleFastaParser(inf):
            seqs.append(seq)
            if prev_start in seq:
                prev_start_count += 1
            if prev_end in seq:
                prev_end_count += 1

def get_base(score_A, score_C, score_G, score_T):
    total = score_A + score_C + score_G + score_T
    if not total:
        return None

    top_base = 'A'
    top_score = score_A
    if score_C > top_score:
        top_base = 'C'
        top_score = score_C
    if score_G > top_score:
        top_base = 'G'
        top_score = score_G
    if score_T > top_score:
        top_base = 'T'
        top_score = score_T

    # Very rough conversion from scores to the counts we were using before.
    count = top_score / K / 2
        
    # These rules could be a lot fancier.  The basic principle is that we'd get
    # the most accuracy by adding only the single most confident base each
    # time, but if we did this we'd need a very large number of iterations.
    # But if we're confident enough about the bases we're adding, though, we
    # can add dozens in a single iteration, making it *much* faster.
    #
    # The main idea is that once enough reads have dropped off we should
    # rescan.
    if (count < 10 or
        count < max(prev_start_count, prev_end_count) / 100):

        sys.stderr.write(
            "%s rejected (max(%s, %s)): %s / %s = %.2f\n" % (
                target, prev_start_count, prev_end_count,
                count, total, count/total))
        return None

    return top_base

# Each time through the loop we look at every read, and if it matches either
# the start or end of the contig we count the distribution of bases.  We take
# the most common base, and keep going.
contig = prev_contig[END_LENGTH:-END_LENGTH]
if len(contig) < len(seed):
    contig = seed

MISMATCH_PENALTY=.9
def score(seq, match_pos, direction):
    # We want to give high scores for sequences that are a good match for our
    # in-progress contig.  This idea is that if we see:
    #
    #  contig:   ABCDEFGHIJK
    #       1:        FGHIJKL
    #       2:        FZHWXKM
    #       3:        YTUVSKN
    #  then L > M > N

    if direction == 1 and False:
        print(seq)
        print("%s%s" % (
            " " * (match_pos), contig))
        print ("%s[%s]" % (
            " " * (match_pos), " " * (K-2)))
    elif direction == -1 and False:
        print(contig)
        print("%s%s" % (
            " " * (len(contig) - K - match_pos), seq))
        print ("%s[%s]" % (
            " " * (len(contig) - K), " " * (K-2)))

    # First, figure out how well seq matches contig.

    # We know that seq[match_pos:match_pos+K] is
    #   if direction == 1:  contig[:K]
    #   if direction == -1: contig[-K:]
    assert(seq[match_pos:match_pos+K] ==
           contig[:K] if direction == 1 else contig[-K:])

    matches = K
    mismatches = 0
    # Now work away from the known match seeing how many other matches there
    # are.
    contig_index = K if direction == 1 else len(contig)-K-1
    seq_index = match_pos + K if direction == 1 else match_pos - 1

    while 0 <= contig_index < len(contig) and 0 <= seq_index < len(seq):
        if False:
            print("%s =? %s" % (contig[contig_index], seq[seq_index]))
        if contig[contig_index] == seq[seq_index]:
            matches += 1
        else:
            mismatches += 1
        contig_index += direction
        seq_index += direction

    if False:
        print(matches, mismatches, matches * MISMATCH_PENALTY**mismatches)

    # How to go from #matches and #mismatches to a score?  Nothing principled
    # here, but the general idea is that more matches is good and more
    # mismatches is bad.  We don't want to go below zero, since even terrible
    # evidence for a base is still not evidence against that base.
    return matches * MISMATCH_PENALTY**mismatches

def run_subprocess(direction):
    proc = subprocess.Popen([iterative_assembler_exe, direction, contig],
                            stdout=subprocess.PIPE,
                            stdin=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True)
    outs, errs = proc.communicate(timeout=15, input="\n".join(seqs))
    if proc.returncode != 0:
        raise Exception("%s failed with exit code %s %r" % (
            proc.returncode, (outs, errs)))

    score_A, score_C, score_G, score_T = outs.strip().split()
    return float(score_A), float(score_C), float(score_G), float(score_T)

need_next = True
need_prev = True
while need_next or need_prev:
    print(contig)
    start = contig[:K]
    end = contig[-K:]

    # We currently don't have any way of assembling around loops of >K, so if
    # we get to a kmer we've seen before just bail.
    if start in contig[1:]:
        need_prev = False
    if end in contig[:-1]:
        need_next = False

    if need_next:
        next_base = get_base(*run_subprocess("n"))
        if next_base:
            contig = contig + next_base
        else:
            need_next = False

    if need_prev:
        prev_base = get_base(*run_subprocess("p"))
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
