#!/usr/bin/env bash

if [ ! -d /run/kmer ]; then
    sudo mkdir /run/kmer
    sudo chown $(whoami) /run/kmer
fi

for a in A C G T; do
    for wtp in $(cat longest-timeseries.tsv | awk '{print $3}' | sort | uniq); do
        echo $a $wtp
        fname_in="clean-TS-ss-$wtp-$a.gz"
        fname_out="clean-TS-ss-$wtp-$a.sorted.gz"
        aws s3 cp "s3://prjna729801/${fname_in}" /run/kmer/
        cat /run/kmer/$fname_in | \
            gunzip | \
            sort -n --parallel=32 --buffer-size=60G -T /run/kmer |
            gzip > /run/kmer/$fname_out
        rm /run/kmer/$fname_in
        aws s3 cp /run/kmer/$fname_out s3://prjna729801/
    done
    echo "computing correlations for $a..."
    for b in A C G T; do
        for c in A C G T; do
            prefix="$a$b$c"
            fname_out="clean-TS-ss-$prefix-correlation.tsv"
            echo $prefix to $fname_out
            ./compute-correlation.py \
                tmp.$prefix.progress \
                $prefix \
                /run/kmer/clean-TS-ss-*-$a.sorted.gz | \
                aws s3 cp - "s3://prjna729801/${fname_out}" &
        done
    done
    wait

    echo "saving and cleaning up $a..."
    for x in /run/kmer/clean-TS-ss-*-$a.sorted.gz; do
        aws s3 cp $x s3://prjna729801/ && rm $x
    done
done
