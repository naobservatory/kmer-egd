import sys

out_prefix, = sys.argv[1:]

for line in sys.stdin:
    biggest_count, bucket, counts = line.strip().split(sep="\t", maxsplit=2)
    counts = counts.split("\t")

    if not days:
        for _ in range(len(counts)):
            days.append([])

    days[counts.index(biggest_count)].append((biggest_count, bucket))

for i, day_data in enumerate(days):
    with open("%s.%s" % (out_prefix, str(i).zfill(2)), "w") as outf:
        for biggest_count, bucket in day_data:
            outf.write("%s\t%s\n" % ( biggest_count, bucket))

