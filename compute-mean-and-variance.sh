#!/bin/bash

for wtp in $(cat longest-timeseries.tsv | awk '{print $3}' | sort | uniq); do
    for a in A C G T; do
        echo "s3://prjna729801/clean-TS-$wtp-$a.gz"
    done
done | xargs -P 32 -I {} ./compute-mean-and-variance-single.sh {}
