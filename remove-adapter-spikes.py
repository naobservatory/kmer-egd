#!/usr/bin/env python3

import os
import sys
import glob

DELETE_THRESHOLD=7

prefix, adapter, fwd_bc, rev_bc = sys.argv[1:]

for fname in glob.glob("%s.*" % prefix):
    with open(fname) as inf:
        try:
            count, contig = next(inf).strip().split()
        except StopIteration:
            # empty file
            os.remove(fname)
            continue

    if adapter in contig:
        index = contig.index(adapter)
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

    elif fwd_bc in contig or rev_bc in contig:
        print("suspicious contig: %s %s" % (fname, contig))
