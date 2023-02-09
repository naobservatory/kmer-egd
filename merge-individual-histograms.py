from glob import glob
from collections import defaultdict

counts = defaultdict(int)
for fname in glob("*-hcu-40-14.tsv.gz.tmp.histcounts"):
    with open(fname) as inf:
        for line in inf:
            count, val = line.strip().split()
            count = int(count)
            val = int(val)

            counts[val] += count

for val, count in sorted(counts.items()):
    print("%s\t%s" % (val, count))
                    
            
