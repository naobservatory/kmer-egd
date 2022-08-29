import sys
from Bio.SeqIO.QualityIO import FastqGeneralIterator

K = 40
DAYS = 14

for sequence_index, (_, sequence, q_) in enumerate(
        FastqGeneralIterator(sys.stdin)):
    for i in range(len(sequence) - K):
        print("%s-%s" % (
            sequence[i:i+K],
            str(sequence_index % DAYS).zfill(2)))
              
