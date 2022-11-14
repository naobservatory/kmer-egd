#!/usr/bin/env python3

import os
import sys
import glob

DELETE_THRESHOLD=7

prefix, adapter = sys.argv[1:]

for fname in glob.glob("%s.*" % prefix):
    with open(fname) as inf:
        count, contig = next(inf).strip().split()

    try:
        index = contig.index(adapter)
    except ValueError:
        continue

    if index < DELETE_THRESHOLD:
        # this "contig" is really an adapter tail and a few bases before it
        os.remove(fname)
        continue

    with open(fname) as inf:
        lines = list(inf)

    trim_index = len(count) + len("\t") + index + len(adapter)
    with open(fname, "w") as outf:
        for line in lines:
            line = line.removesuffix("\n")

            if len(line) > trim_index:
                line = line[:trim_index]

            outf.write("%s\n" % line)
