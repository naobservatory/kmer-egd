import sys
import re
from collections import defaultdict, Counter

K=28

def start(identity):
    lines = set(line.strip() for line in sys.stdin)
    index = 0
    while True:
        contig = assemble(lines)
        if not contig:
            break
        pos_removed = remove_close_matches(contig, lines)
        pos_removed.sort()

        if not pos_removed:
            break

        with open("%s.%s" % (identity, index), "w") as outf:
            outf.write(contig + "\n")
            for pos, removal in pos_removed:
                outf.write("%s%s\n" % (" "*pos, removal))

        index += 1


    if lines:
        with open("%s.unmatched" % identity, "w") as outf:
            for line in lines:
                outf.write("%s\n" % line)

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

def num_base_matches(s1, s2):
    count = 0
    for c1, c2 in zip(s1, s2):
        if c1 == c2:
            count += 1
    return count

def remove_close_matches(contig, lines):
    to_remove = set()
    pos_remove = []
    for raw_line in lines:
        for line in [raw_line, rc(raw_line)]:
            best_pos = None
            best_score = 0
            for pos in range(len(contig) - len(line) + 1):
                score = num_base_matches(contig[pos : pos + len(line)], line)
                if best_pos is None or score > best_score:
                    best_pos = pos
                    best_score = score

            if best_score / len(line) < 0.9: continue

            to_remove.add(raw_line)
            pos_remove.append((best_pos, line))

    lines.difference_update(to_remove)
    return pos_remove

if __name__ == "__main__":
    start(*sys.argv[1:])
