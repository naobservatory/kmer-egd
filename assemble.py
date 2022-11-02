import sys
import re
from collections import defaultdict, Counter
from Bio import Align

K=28

def start(identity):
    lines = set(line.strip() for line in sys.stdin)
    index = 0
    while True:
        contig = assemble(lines)
        if not contig:
            break
        print(contig)
        pos_removed = remove_close_matches(contig, lines)
        pos_removed.sort()

        with open("%s.%s" % (identity, index), "w") as outf:
            for pos, removal in pos_removed:
                outf.write("%s%s\n" % (" "q*pos, removal))

        index += 1

def rc(s):
    return "".join({'T':'A',
                    'G':'C',
                    'A':'T',
                    'C':'G'}[x] for x in reversed(s))

def assemble(lines):
    kmers = Counter()
    prv = defaultdict(Counter)
    nxt = defaultdict(Counter)

    for raw_line in lines:
        for line in [raw_line, rc(raw_line)]:
            for i in range(1, len(line) - K):
                kmer = line[i:i+K]
                prv[kmer][line[i-1]] += 1
                nxt[kmer][line[i+K]] += 1
                kmers[kmer] += 1

    if not kmers:
        return None

    (seed, seed_count), = kmers.most_common(1)
    return assemble_seed(seed, kmers, nxt, prv)

def assemble_seed(seed, kmers, nxt, prv):
    contig = seed

    while True:
        kmer = contig[:K]
        if kmer not in prv: break
        (base, count), = prv[kmer].most_common(1)
        contig = base + contig
        del prv[kmer]

    while True:
        kmer = contig[-K:]
        if kmer not in nxt: break
        (base, count), = nxt[kmer].most_common(1)
        contig = contig + base
        del nxt[kmer]

    return contig

def remove_close_matches(contig, lines):
    aligner = Align.PairwiseAligner()
    # These are the scoring settings porechop uses by default.
    # https://github.com/rrwick/Porechop/blob/master/porechop/porechop.py#L145
    aligner.end_gap_score = 0
    aligner.match_score = 3
    aligner.mismatch_score = -6
    aligner.internal_open_gap_score = -5
    aligner.internal_extend_gap_score = -2

    to_remove = set()
    pos_remove = []
    for raw_line in lines:
        for line in [raw_line, rc(raw_line)]:
            alignment = aligner.align(contig, line)[0]
            score = alignment.score / len(line)
            if score < 2.5: continue

            to_remove.add(raw_line)

            seq1, _, seq2, _ = str(alignment).split('\n')
            matches = re.findall("^-*", seq2)
            pos = len(matches[0]) if matches else 0
            pos_remove.append((pos, line))

    lines.difference_update(to_remove)
    return pos_remove

if __name__ == "__main__":
    start(*sys.argv[1:])
