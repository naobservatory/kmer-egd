#!/bin/bash

for wtp in $(cat longest-timeseries.tsv | awk '{print $3}' | sort | uniq); do
    for a in A C G T; do
        echo "s3://prjna729801/clean-TS-ss-$wtp-$a.gz"
    done
done | xargs -P 32 -I {} ./compute-mean-and-variance-single.sh {}


for wtp in $(cat longest-timeseries.tsv | awk '{print $3}' | sort | uniq); do
    cat <(aws s3 cp "s3://prjna729801/clean-TS-ss-$wtp-A-mvl.tsv" -) \
        <(aws s3 cp "s3://prjna729801/clean-TS-ss-$wtp-C-mvl.tsv" -) \
        <(aws s3 cp "s3://prjna729801/clean-TS-ss-$wtp-G-mvl.tsv" -) \
        <(aws s3 cp "s3://prjna729801/clean-TS-ss-$wtp-T-mvl.tsv" -) | \
        ./merge-per-prefix-counts.py | \
        aws s3 cp - "s3://prjna729801/clean-TS-ss-$wtp-mvl-uniq-c.tsv"
done
