#!/usr/bin/env bash

# Assumes find-best-seeds.sh has already run

cat best-seeds.tsv | while read target count seed; do
    # This is a hack to adjust for the problems:
    #  * we determined the seed counts based on single sites, but there are
    #    actually four sites.
    #  * we determined the seed counts on subsampled data, but the real data is
    #    about 3x bigger.
    count=$(($count*4*3))
    echo Assembling $target from $seed
    ./iterative-assembler.sh \
        ${target/.fasta/} \
        $seed \
        $count \
        $(cat longest-timeseries.tsv | awk '{print $1}')
done
