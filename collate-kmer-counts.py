#!/usr/bin/env python3

import sys
seq_fname, = sys.argv[1:]

K=40

kmer_to_index = {}
kmers = []
with open(seq_fname) as inf:
    for line in inf:
        seq = line.strip()
        for i in range(len(seq) - K + 1):
            kmer = seq[i:i+K]
            if kmer in kmer_to_index:
                raise Exception("duplicate: %s at both %s and %s" % (
                    kmer, kmer_to_index[kmer], i))
            kmer_to_index[kmer] = i
            kmers.append(kmer)

data = [None] * len(kmers)
data_rc = [None] * len(kmers)

def rc(s):
    return "".join({'T':'A',
                    'G':'C',
                    'A':'T',
                    'C':'G',
                    'N':'N'}[x] for x in reversed(s))

for line in sys.stdin:
    cols = line.strip().split()
    kmer, cols = cols[0], cols[1:]
    kmer_rc = rc(kmer)

    cols = [int(x) for x in cols]
        
    index_fwd = kmer_to_index.get(kmer, None)
    index_rev = kmer_to_index.get(kmer_rc, None)

    if index_fwd is None and index_rev is None:
        raise Exception("Unknown kmer %s" % kmer)
    if index_fwd is not None and index_rev is not None:
        # Can't do anything with these right now
        continue
    
    if index_fwd is not None:
        index = index_fwd
        chosen_kmer = kmer
        chosen_data = data
    else:
        index = index_rev
        chosen_kmer = kmer_rc
        chosen_data = data_rc

    if chosen_data[index] is not None:
        raise Exception("Got %s and %s" % (chosen_data[index], cols))
    
    chosen_data[index] = [chosen_kmer] + cols

for index, (cols, cols_rc) in enumerate(zip(data, data_rc)):
    if cols is None and cols_rc is None:
        continue
        
    row = [index] + cols + cols_rc
    print("\t".join(str(x) for x in row))
    
