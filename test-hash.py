#!/usr/bin/env python3
import subprocess

fwd_hashes = {}
rev_hashes = {}

for line in subprocess.check_output("./test-hash").split(b"\n"):
    line = line.strip()
    if not line: continue
    fwd_rev, h, seq = line.split(b'\t')

    fwd_rev = fwd_rev.decode('utf8')
    h = int(h)
    seq = seq.decode('utf8')
    
    if fwd_rev == 'F':
        fwd_hashes[seq] = h
    elif fwd_rev == 'R':
        rev_hashes[seq] = h
    else:
        raise Exception("Bad line: %r" % line)
    
def rc(kmer):
    return ''.join(
        [{'A': 'T',
          'C': 'G',
          'G': 'C',
          'T': 'A'}[x]
         for x in kmer[::-1]])

if len(fwd_hashes) != len(rev_hashes):
    raise Exception("Different number of hashes")

for seq, h in fwd_hashes.items():
    rseq = rc(seq)
    if rseq not in rev_hashes:
        raise Exception("Missing %r" % rseq)
    elif rev_hashes[rseq] != h:
        raise Exception("Disagreement %s vs %s for %r and %r" % (
            h, rev_hashes[rseq], seq, rseq))
        
print("PASS")
