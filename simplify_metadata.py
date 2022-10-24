data = []

with open("rothman.unenriched_samples") as inf:
    for line in inf:
        fname = line.split("_")[0]
        wtp = line.split()[1].split("_")[0]
        month = line.split()[1].split("_")[1]
        day = line.split()[1].split("_")[2]
        year = line.split()[1].split("_")[3]

        if len(year) == 2:
            year = '20%s' % year

        data.append((wtp, "%s-%s-%s" % (
            year, month.zfill(2), day.zfill(2)), fname))

for wtp, date, fname in sorted(data):
    print("%s\t%s\t%s" % (
        fname, date, wtp))
