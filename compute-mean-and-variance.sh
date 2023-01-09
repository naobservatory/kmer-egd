#!/bin/bash

for wtp in $(cat longest-timeseries.tsv | awk '{print $3}' | sort | uniq); do
    for a in A C G T; do
        echo "s3://prjna729801/clean-TS-$wtp-$a.gz"
    done
done | xargs -P 32 -I {} ./compute-mean-and-variance-single.sh {}

sudo mkdir /run/kmer
sudo chown $whoami /run/kmer

for wtp in $(cat longest-timeseries.tsv | awk '{print $3}' | sort | uniq); do
    aws s3 cp "s3://prjna729801/clean-TS-$wtp-A-mv.gz" /var/run/kmer
    aws s3 cp "s3://prjna729801/clean-TS-$wtp-C-mv.gz" /var/run/kmer
    aws s3 cp "s3://prjna729801/clean-TS-$wtp-T-mv.gz" /var/run/kmer
    aws s3 cp "s3://prjna729801/clean-TS-$wtp-G-mv.gz" /var/run/kmer
    cat /var/run/kmer/clean-TS-$wtp-A-mv.gz \
        /var/run/kmer/clean-TS-$wtp-C-mv.gz \
        /var/run/kmer/clean-TS-$wtp-T-mv.gz \
        /var/run/kmer/clean-TS-$wtp-G-mv.gz | \
        sort -n --parallel=32 --buffer-size=60G -T /run/kmer | \
        uniq -c | \
        aws s3 cp - "s3://prjna729801/clean-TS-$wtp-mv-uniq-c.gz"
    rm /var/run/kmer/clean-TS-$wtp-*-mv.gz
done
