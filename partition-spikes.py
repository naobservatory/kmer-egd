import sys

day, = sys.argv[1:]

for line in sys.stdin:
    biggest_count, bucket, counts = line.strip().split(sep="\t", maxsplit=2)
    counts = counts.split("\t")

    if counts.index(biggest_count) == int(day):
        print("%s\t%s" % (biggest_count, bucket))
