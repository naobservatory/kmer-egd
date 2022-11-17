#!/usr/bin/env python3

import os
import sys
import glob
from Bio import Align

# Discard contigs that have this few bases left after removing adapters
DISCARD_THRESHOLD=12

# Minimum trailing bases to trim if the contig ends with something trimmable.
# We don't want to say no contigs can end with "CT" just because the adapters
# start with CT.
TRIM_THRESHOLD=6

prefix, p5_adapter_rc, p7_adapter_rc = sys.argv[1:]

# Because we're using a two color system reads that go off the end will see
# lots of G, so there's a sense in which adapters "end" with strings of G.
p5_adapter_rc += "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"
p7_adapter_rc += "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"

# Find the P5 or P7 adapter
def adapter_index(contig):
    best_index = None
    best_score = TRIM_THRESHOLD * 3 - 1 # minimum score to accept
    best_adapter = None
    best_alignment = None

    for adapter in [p5_adapter_rc, p7_adapter_rc]:
        aligner = Align.PairwiseAligner()
        # These are the scoring settings porechop uses by default.
        # https://github.com/rrwick/Porechop/blob/master/porechop/porechop.py#L145
        aligner.end_gap_score = 0
        aligner.match_score = 3
        aligner.mismatch_score = -6
        aligner.internal_open_gap_score = -5
        aligner.internal_extend_gap_score = -2

        alignment = aligner.align(contig, adapter)[0]
        score = alignment.score

        if score > best_score:
            best_score = score

            contig_locs, adapter_locs = alignment.aligned
            contig_index_start, contig_index_end = contig_locs[0]

            best_index = contig_index_start
            best_adapter = adapter
            best_alignment = alignment

    #if best_index is not None:
    #    print("Match at %s, score=%.2f" % (best_index, best_score))
    #    print(best_alignment)

    return best_index

for fname in glob.glob("%s.*" % prefix):
    with open(fname) as inf:
        try:
            count, contig = next(inf).strip().split()
        except StopIteration:
            # empty file
            os.remove(fname)
            continue

    index = adapter_index(contig)
    if index is None:
        continue

    if index < DISCARD_THRESHOLD:
        # this "contig" is really an adapter tail and a few bases before it
        os.rename(fname, fname.replace("spike", "barcode"))
        continue

    with open(fname) as inf:
        lines = list(inf)

        trim_index = len(count) + len("\t") + index
        with open(fname, "w") as outf:
            for line in lines:
                line = line.removesuffix("\n")

                if len(line) > trim_index:
                    line = line[:trim_index]

                    outf.write("%s\n" % line)
