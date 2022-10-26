import sys
import glob
from collections import defaultdict

def start(prefix):
    total = 0
    seen_n_days = defaultdict(int)
    seen_nth_popular = defaultdict(int)

    for fname in glob.glob("%s-*.summary" % prefix):
        with open(fname) as inf:
            for line in inf:
                line = line.strip()
                if not line: continue

                if line.count("\t") == 0:
                    total += int(line)

                elif line.count("\t") == 1:
                    n_days, count = line.split("\t")
                    seen_n_days[int(n_days)] += int(count)

                elif line.count("\t") == 2:
                    pos, logval, count = line.split("\t")
                    seen_nth_popular[int(pos), int(logval)] += int(count)

                else:
                    raise Exception("bad input %r" % line)

    print(total)
    print()

    for n_days, count in sorted(seen_n_days.items()):
        print("%s\t%s" % (n_days, count))
    print()
    
    for (pos, logval), count in sorted(seen_nth_popular.items()):
        print("%s\t%s\t%s" % (pos, logval, count))

if __name__ == "__main__":
    start(*sys.argv[1:])


