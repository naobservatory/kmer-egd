#!/usr/bin/env python3

# cat longest-timeseries.tsv | awk '{print $1"_1\n"$1"_2"}' | \
# xargs -P 32 -I {} bash -c \
#   "aws s3 cp s3://prjna729801/{}.fastq.gz - | gunzip | \
#      python3 determine-read-contig-starts.py fasta/*2023-02-06.fasta > \
#      ../2023-02-09--read-contig-starts/{}.json"

import os
import sys
import json
from collections import Counter, defaultdict
from Bio.SeqIO.FastaIO import SimpleFastaParser
from Bio.SeqIO.QualityIO import FastqGeneralIterator

contig_fastas = sys.argv[1:]

K=40

def rc(s):
    return "".join({'T':'A', 'G':'C', 'A':'T', 'C':'G', 'N':'N'}[x]
                   for x in reversed(s))

def kmers(seq):
    for i in range(len(seq) - K + 1):
        yield seq[i:i+K]

"""
First, the simple case, where we match in forward.  We have a long contig,
which is partially matched by a read on the basis of at least one k-mer
match.  The kmer is in position p along read, and matches position L along
contig.  We want to report G, the place the read started, so we need to move
backwards from L along contig by the offset within read.  That offset is p,  so
we compute L-p.

      G  L
 |====================== contig ==========================|
      |---- read ----|
         |k|
         p

Next, the harder case, where we match in reverse.  The reverse complement of
the read has a k-mer matching position L along the contig.  We want to
report G, the place the read started, so need to move forwards from L along
contig adjusting for the remaining length of the read.  This means we want L +
len(read) - p - 1.

         L            G
 |====================== contig ==========================|
      |--- rc read ---|
         |k|
         p
"""

dups = set()
kmer_to_vid_loc = {} # kmer -> vid, loc_start

vid_counts = defaultdict(Counter) # vid -> f/r + loc -> count

for contig_fasta in contig_fastas:
    vid = os.path.basename(contig_fasta).replace(".fasta", "")
    with open(contig_fasta) as inf:
        (_, seq), = SimpleFastaParser(inf)
        for loc, kmer in enumerate(kmers(seq)):
            if kmer in kmer_to_vid_loc:
                dups.add(kmer)
            kmer_to_vid_loc[kmer] = vid, loc

for dup in dups:
    del kmer_to_vid_loc[dup]

def interpret_read(seq, is_rc):
    cur_vid = None
    locs = Counter()
    for pos, kmer in enumerate(kmers(seq)):
        vid, loc = kmer_to_vid_loc.get(kmer, (None, None))
        if not vid: continue
        if cur_vid and vid != cur_vid: return None, None
        cur_vid = vid
        if is_rc:
            locs[loc + len(seq) - pos - 1] += 1
        else:
            locs[loc - pos] += 1

    if not cur_vid: return None, None

    loc, _ = locs.most_common()[0]
    return cur_vid, loc

for  _, seq, _ in FastqGeneralIterator(sys.stdin):
    vid_f, loc_f = interpret_read(seq, is_rc=False)
    vid_r, loc_r = interpret_read(rc(seq), is_rc=True)

    if vid_f and vid_r: continue
    if vid_f:
        vid_counts[vid_f]["f%s" % loc_f] += 1
    elif vid_r:
        vid_counts[vid_r]["r%s" % loc_r] += 1

print(json.dumps(vid_counts))
