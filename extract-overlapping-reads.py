#!/usr/bin/env python3
import os
import sys
import glob
from Bio.SeqIO.QualityIO import FastqGeneralIterator

accession, seeds_file = sys.argv[1:]

K=40
END_LENGTH=100

def rc(s):
    return "".join({'T':'A',
                    'G':'C',
                    'A':'T',
                    'C':'G',
                    'N':'N'}[x] for x in reversed(s))

# kmer -> [target, should_rc]
to_find = {}
def search_for_rc(kmer, target, should_rc):
    if kmer in to_find:
        to_find[kmer] = None, None
    else:
        to_find[kmer] = target, should_rc

def search_for(kmer, target):
    search_for_rc(kmer, target, False)
    search_for_rc(rc(kmer), target, True)

def kmers(seq):
    for i in range(len(seq) - K + 1):
        yield seq[i:K+i]

files = {}
with open(seeds_file) as inf:
    for line in inf:
        target = line.split(".fasta")[0]

        if os.path.exists("%s/final_contig.seq" % target):
            continue

        iteration = max(int(fname.split("/")[-1].split(".")[0])
                        for fname in glob.glob("%s/*.contig.seq" % target))

        target_seq_fname = "%s/%s.contig.seq" % (target, iteration)

        files[target] = open(
            "%s/%s.%s.fasta" % (target, accession, iteration), "w")
        with open(target_seq_fname) as seqf:
            contig, = seqf
            contig = contig.strip()

            # As we keep iterating the middle of the contig is eventually
            # settled, and we only care about the ends. If it's a short contig,
            # extract reads matching anywhere, but if it's a long contig
            # extract only for the ends.
            if len(contig) <= (END_LENGTH+K)*2:
                for kmer in kmers(contig):
                    search_for(kmer, target)
            else:
                for kmer in kmers(contig[:END_LENGTH+K]):
                    search_for(kmer, target)
                for kmer in kmers(contig[-(END_LENGTH+K):]):
                    search_for(kmer, target)

for title, seq, quality in FastqGeneralIterator(sys.stdin):
    targets = {} # target -> should_rc
    for kmer in kmers(seq):
        target, should_rc = to_find.get(kmer, (None, None))
        if target:
            targets[target] = should_rc
    for target, should_rc in targets.items():
        files[target].write(
            ">%s%s\n%s\n" % (
                title,
                ":rc" if should_rc else "",
                rc(seq) if should_rc else seq,
            ))
