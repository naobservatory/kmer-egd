#!/usr/bin/python3

import sys
import glob

day, parity = sys.argv[1:]

kmers = {} # kmer -> contig

K = None

def rc(s):
    return "".join({'T':'A',
                    'G':'C',
                    'A':'T',
                    'C':'G',
                    'N':'N'}[x] for x in reversed(s))

for spike_contig_fname in glob.glob("hc-HTP-spike-contigs.%s.*" % day):
    suffix = spike_contig_fname.split(".")[-1]
    if suffix == "unmatched": continue

    total = None
    with open(spike_contig_fname) as inf:
        for i, line in enumerate(inf):
            if i == 0:
                count, contig = line.strip().split()
            else:
                try:
                    count, kmer = line.strip().split()
                except ValueError:
                    # expected from remove-adapter-spikes.py trimming
                    continue

                if K is None:
                    K = len(kmer)
                elif K != len(kmer):
                    # expected from remove-adapter-spikes.py trimming
                    continue
                kmers[kmer] = suffix

# suffix -> file
files = {}
for suffix in kmers.values():
    if suffix not in files:
        files[suffix] = open("hc-HTP-spike-reads.%s.%s.%s" % (day, parity, suffix), 'w')

for lineno, line in enumerate(sys.stdin):
    if lineno % 10000000 == 0:
        print("%s:%s..." % (day, lineno))

    if not line or line[0] not in 'ACGT': continue
    line = line.strip()
    written = set()
    for rd in [line, rc(line)]:
        for i in range(len(rd)-K+1):
            kmer = rd[i:i+K]
            suffix = kmers.get(kmer, None)
            if suffix and suffix not in written:
                files[suffix].write(line)
                files[suffix].write("\n")
                written.add(suffix)
