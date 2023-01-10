#!/usr/bin/env python3

import sys
import gzip
import time
from collections import Counter

progress_file, prefix, *fnames = sys.argv[1:]
files = [gzip.open(fname, "rt") for fname in fnames]

DUMP_INTERVAL=10000000

def read_kmer(f):
    while True:
        try:
            line = next(f)
        except StopIteration:
            return None, None
        kmer, samples = line.strip().split("\t", 1)

        if kmer.startswith(prefix):
            break

    samples = [int(x) for x in samples.split("\t")]
    return kmer, samples

nexts = [read_kmer(f) for f in files]
cur_kmer = min(x[0] for x in nexts)

global_corr_total_unweighted = Counter()
global_corr_total_mean_weighted = Counter()
global_corr_total_mean2_weighted = Counter()
global_corr_count = Counter()

wtp_corr_total_unweighted = Counter()
wtp_corr_total_mean_weighted = Counter()
wtp_corr_total_mean2_weighted = Counter()
wtp_corr_count = Counter()

last_progress_dump = 0

def get_status():
    rows = []
    for key in sorted(global_corr_count):
        rows.append("\t".join(
            str(x) for x in [
                "\t".join(str(y) for y in key),
                global_corr_total_unweighted[key],
                global_corr_total_mean_weighted[key],
                global_corr_total_mean2_weighted[key],
                global_corr_count[key],
                wtp_corr_total_unweighted[key],
                wtp_corr_total_mean_weighted[key],
                wtp_corr_total_mean2_weighted[key],
                wtp_corr_count[key]]))
    return "\n".join(rows)

while True:
    all_samples = []
    for kmer, samples in nexts:
        if kmer == cur_kmer:
            all_samples.append(samples)
        else:
            all_samples.append([])

    all_total = 0
    all_count = 0

    means = []

    for samples in all_samples:
        this_total = sum(samples)
        this_count = len(samples)

        all_total += this_total
        all_count += this_count

        if this_count == 0:
            means.append(0)
        else:
            means.append(this_total / this_count)

    mean = all_total / all_count

    for wtp_idx_1, samples_1 in enumerate(all_samples):
        # do want to include same-wtp comparision, but no need to do cross-wtp
        # comparision twice
        for wtp_idx_2, samples_2 in enumerate(all_samples[wtp_idx_1:]):
            for sample_idx_1, sample_1 in enumerate(samples_1):
                for sample_idx_2, sample_2 in enumerate(samples_2[sample_idx_1:]):
                    key = wtp_idx_1, wtp_idx_2, sample_idx_1, sample_idx_2

                    global_adjusted_1 = sample_1 - mean
                    global_adjusted_2 = sample_2 - mean

                    global_product = global_adjusted_1 * global_adjusted_2
                    global_mean_weighted = global_product / mean
                    global_mean2_weighted = global_mean_weighted / mean

                    global_corr_total_unweighted[key] += global_product
                    global_corr_total_mean_weighted[key] += global_mean_weighted
                    global_corr_total_mean2_weighted[key] += global_mean2_weighted
                    global_corr_count[key] += 1

                    if wtp_idx_1 != wtp_idx_2:
                        continue

                    wtp_mean = means[wtp_idx_1]
                    if not wtp_mean:
                        continue

                    wtp_adjusted_1 = sample_1 - wtp_mean
                    wtp_adjusted_2 = sample_2 - wtp_mean

                    wtp_product = wtp_adjusted_1 * wtp_adjusted_2
                    wtp_mean_weighted = wtp_product / wtp_mean
                    wtp_mean2_weighted = wtp_mean_weighted / wtp_mean

                    wtp_corr_total_unweighted[key] += wtp_product
                    wtp_corr_total_mean_weighted[key] += wtp_mean_weighted
                    wtp_corr_total_mean2_weighted[key] += wtp_mean2_weighted
                    wtp_corr_count[key] += 1

    for i, samples in enumerate(all_samples):
        if samples:
            nexts[i] = read_kmer(files[i])

    if all(x[0] is None for x in nexts): break
    cur_kmer = min(x[0] for x in nexts if x[0] is not None)

    progress = sum(wtp_corr_count.values())
    if progress - last_progress_dump > DUMP_INTERVAL:
        with open(progress_file, "w") as outf:
            outf.write(time.time())
            outf.write(get_status())
            outf.write("\n")
        last_progress_dump = progress

print(get_status())
