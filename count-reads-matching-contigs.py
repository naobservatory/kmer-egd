#!/usr/bin/env python3

# cat longest-timeseries.tsv | awk '{print $1}' | tr ' ' '\n' | \
# xargs -P 32 -I {} bash -c \
#   "aws s3 cp s3://prjna729801/{}.arclean.fastq.gz - | gunzip | \
#      python3 count-reads-matching-contigs.py *2023-02-06.fasta > \
#      2023-02-07--top-counts/{}.json"

import os
import sys
import json
from collections import Counter
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

dups = set()
kmer_to_vid = {}
vid_counts = Counter()

for contig_fasta in contig_fastas:
    vid = os.path.basename(contig_fasta).replace(".fasta", "")
    with open(contig_fasta) as inf:
        (_, seq), = SimpleFastaParser(inf)
        for s in [seq, rc(seq)]:
            for kmer in kmers(s):
                if kmer in kmer_to_vid:
                    dups.add(kmer)
                kmer_to_vid[kmer] = vid

for dup in dups:
    del kmer_to_vid[dup]

for  _, seq, _ in FastqGeneralIterator(sys.stdin):
    seen = set()
    for kmer in kmers(seq):
        vid = kmer_to_vid.get(kmer, None)
        if vid:
            seen.add(vid)
    if len(seen) == 1:
        vid, = seen
        vid_counts[vid] += 1

print(json.dumps(vid_counts))
        
