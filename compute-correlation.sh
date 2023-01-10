#!/usr/bin/env bash

for a in A C T G; do
    for wtp in $(cat longest-timeseries.tsv | awk '{print $3}' | sort | uniq); do
        echo $a $wtp
        fname_in="clean-TS-$wtp-$a.gz"
        fname_out="clean-TS-$wtp-$a.sorted.gz"
        aws s3 cp "s3://prjna729801/${fname_in}" /run/kmer/
        cat /run/kmer/$fname_in | \
            gunzip | \
            sort -n --parallel=32 --buffer-size=60G -T /run/kmer |
            gzip > /run/kmer/$fname_out
        rm /run/kmer/$fname_in
    done
    echo "computing correlatios for $a..."
    ./compute-correlation.py /run/kmer/clean-TS-*-$a.sorted.gz | \
        aws s3 cp - "s3://prjna729801/clean-TS-$a-correlation.tsv"
    echo "saving and cleaning up $a..."
    for x in /run/kmer/clean-TS-*-$a.sorted.gz; do
        aws s3 cp $x s3://prjna729801/ && rm $x
    done
done

