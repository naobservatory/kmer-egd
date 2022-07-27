import sys
from Bio.SeqIO.QualityIO import FastqGeneralIterator
import numpy as np

K = 40

if len(sys.argv) != 2:
    print("Usage: count-kmer-eqs.py N_BUCKETS")
    sys.exit(1)

buckets = np.zeros(int(sys.argv[1]), dtype=np.uint32)
max_val = 2**32

COMPLEMENT = {
    'A': 'T',
    'C': 'G',
    'G': 'C',
    'T': 'A',
}

for _, seq, _ in FastqGeneralIterator(sys.stdin):
    for i in range(len(seq) - K):
        kmer = seq[i:i+K]
        kmer_rc = ''.join([COMPLEMENT.get(x,x) for x in kmer[::-1]])
        if kmer_rc < kmer:
            kmer = kmer_rc
        h = hash(kmer)
        idx = hash(kmer) % len(buckets)
        val = buckets[idx]
        if val < max_val:
            buckets[idx] = val + 1

for val in buckets:
    print("%s" % val)
