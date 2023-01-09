#!/bin/bash

for wtp in $(cat longest-timeseries.tsv | awk '{print $3}' | sort | uniq); do
    for a in A C G T; do
        echo "s3://prjna729801/clean-TS-$wtp-$a.gz"
    done
done | xargs -P 32 -I {} ./compute-mean-and-variance-single.sh {}

for wtp in $(cat longest-timeseries.tsv | awk '{print $3}' | sort | uniq); do
    for a in A C G T; do
        aws s3 cp "s3://prjna729801/clean-TS-$wtp-$a-mv.gz" - | \
            uniq | \
            gzip | \
            aws s3 cp - "s3://prjna729801/clean-TS-$wtp-$a-mv-uniq.gz"
    done
done

for wtp in $(cat longest-timeseries.tsv | awk '{print $3}' | sort | uniq); do
    cat <(aws s3 cp "s3://prjna729801/clean-TS-$wtp-A-mv-uniq.gz" -| gunzip) \
        <(aws s3 cp "s3://prjna729801/clean-TS-$wtp-C-mv-uniq.gz" -| gunzip) \
        <(aws s3 cp "s3://prjna729801/clean-TS-$wtp-G-mv-uniq.gz" -| gunzip) \
        <(aws s3 cp "s3://prjna729801/clean-TS-$wtp-T-mv-uniq.gz" -| gunzip) | \
        sort -n | \
        uniq | \
        aws s3 cp - "s3://prjna729801/clean-TS-$wtp-mv-uniq.gz"
done

for wtp in $(cat longest-timeseries.tsv | awk '{print $3}' | sort | uniq); do
    cat <(aws s3 cp "s3://prjna729801/clean-TS-$wtp-A-mv.gz" - ) \
        <(aws s3 cp "s3://prjna729801/clean-TS-$wtp-C-mv.gz" - ) \
        <(aws s3 cp "s3://prjna729801/clean-TS-$wtp-G-mv.gz" - ) \
        <(aws s3 cp "s3://prjna729801/clean-TS-$wtp-T-mv.gz" - ) | \
        sort -n | \
        uniq -c | \
        aws s3 cp - "s3://prjna729801/clean-TS-$wtp-mv-uniq-c.gz"
done
