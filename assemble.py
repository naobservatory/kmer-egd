import sys
import re
from collections import defaultdict, Counter

K=28

def start(identity):
    lines = Counter()
    for line in sys.stdin:
        line = line.strip()
        if '\t' in line:
            count, line = line.split("\t")
            count = int(count)
        else:
            count = 1
        lines[line] += count

    print("Assembling %s (%s reads)..." % (identity, len(lines)))

    index = 0
    while True:
        contig = assemble(lines)
        if not contig:
            break
        pos_removed = remove_close_matches(contig, lines)
        if not pos_removed:
            break

        with open("%s.%.3d" % (identity, index), "w") as outf:
            outf.write("%.12d\t%s\n" % (
                sum(count for _, _, count in pos_removed),
                contig))
            pos_removed.sort()
            for pos, removal, count in pos_removed:
                outf.write("%.12d\t%s%s\n" % (count, " "*pos, removal))

        index += 1


    if lines:
        with open("%s.unmatched" % identity, "w") as outf:
            for line, count in lines.items():
                outf.write("%s\t%s\n" % (count, line))

def rc(s):
    return "".join({'T':'A',
                    'G':'C',
                    'A':'T',
                    'C':'G',
                    'N':'N'}[x] for x in reversed(s))

def assemble(lines):
    prv = defaultdict(Counter)
    nxt = defaultdict(Counter)

    for raw_line, count in lines.items():
        for line in [raw_line, rc(raw_line)]:
            for i in range(1, len(line) - K):
                kmer = line[i:i+K]
                prv[kmer][line[i-1]] += count
                nxt[kmer][line[i+K]] += count

    if not prv:
        return None

    # find most common kmer to use as seed
    max_count = 0
    kmer_max_count = None
    for kmer, bases in prv.items():
        count = sum(bases.values())
        if count > max_count:
            max_count = count
            kmer_max_count = kmer

    return assemble_seed(kmer, nxt, prv)

def assemble_seed(seed, nxt, prv):
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
    for raw_line, count in lines.items():
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
            pos_remove.append((best_pos, line, count))

    for raw_line in to_remove:
        del lines[raw_line]

    return pos_remove

if __name__ == "__main__":
    start(*sys.argv[1:])
