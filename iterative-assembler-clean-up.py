#!/usr/bin/env python3

import os
import sys
import glob
from Bio.SeqIO.FastaIO import SimpleFastaParser
from collections import Counter, defaultdict

target, = sys.argv[1:]
iteration = max(int(fname.split("/")[-1].split(".")[0])
                for fname in glob.glob("%s/*.contig.seq" % target))

for fname in glob.glob("%s/*.*.fasta" % target):
    fname_iteration = int(fname.split(".")[-2])
    if fname_iteration < iteration:
        os.remove(fname)
