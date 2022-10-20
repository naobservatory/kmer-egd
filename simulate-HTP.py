import statsmodels.api as sm
import datetime
import math

data = []

first_date = None
with open("rothman-covid-counts") as inf:
    for line in inf:
        line = line.strip()
        wtp, date, total_reads, covid_reads, cases_per_100k = line.split('\t')
        if wtp != "HTP": continue

        total_reads = int(total_reads)
        covid_reads = int(covid_reads)
        cases_per_100k = int(cases_per_100k)

        parsed_date = datetime.datetime.strptime(date, "%Y-%m-%d")
        if first_date is None:
            first_date = parsed_date

        date_offset = (parsed_date - first_date).days

        data.append([date_offset, covid_reads, date_offset,
                     date, total_reads, cases_per_100k])

xs = [x[0] for x in data]
ys = [x[1] for x in data]

for i in range(5, len(data)):
    vals = xs[:i]
    days = ys[:i]
    
    model = sm.GLM(vals, sm.add_constant(days),
                   family=sm.families.Poisson())

    try:
        result = model.fit()
    except ValueError:
        continue
    
    pvalue = result.pvalues[1]
    coef = result.params[1]

    coef = math.exp(coef)-1

    print("%s (%sd)\t%.4e\t%.1f%%" % (data[i][3], data[i][2], pvalue, coef*100))
