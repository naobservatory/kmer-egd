import sys
import hashlib
import Bio.SeqIO

if len(sys.argv) not in [1, 2]:
    print("Usage: cat foo.fasta | %s [hash_denom]")
    sys.exit(1)

hash_denom = 1
if len(sys.argv) == 2:
    hash_denom = int(sys.argv[1])

K = 40
for record in Bio.SeqIO.parse(sys.stdin, "fasta"):
    for i in range(len(record.seq) - K):
        kmer = record.seq[i:i+K]
        if hash_denom > 1:
            digest = hashlib.sha256(bytes(kmer)).digest()
            if int.from_bytes(digest[:4], "big") % hash_denom != 0:
                continue
        
        print(kmer)
