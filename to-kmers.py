import sys
import Bio.SeqIO

K = 40
for record in Bio.SeqIO.parse(sys.stdin, "fasta"):
    for i in range(len(record.seq) - K):
        print(record.seq[i:i+K])
