#!/bin/bash

for wtp in $(cat longest-timeseries.tsv | awk '{print $3}' | sort | uniq); do
  for a in A C G T; do
    fname_out="s3://prjna729801/clean-TS-ss-$wtp-$a.gz"

    #if aws s3 ls "$fname_out" > /dev/null ; then
    #    continue
    #fi

    echo "... $wtp $a"
    time cat longest-timeseries.tsv | \
        awk -F '\t' '$3=="'$wtp'"{print $1}' | \
        xargs -P1 -I {} aws s3 cp s3://prjna729801/{}.arclean.fastq.gz - | \
        gunzip | \
        sed -E 's/^@MT?_/@/' | \
        ./hash-count-rothman \
            $wtp \
            $a \
            longest-timeseries-with-lengths.tsv \
            $(cat longest-timeseries-with-lengths.tsv | \
                  awk '{print $NF}' | \
                  sort -n | \
                  head -n 1) | \
        gzip | \
        aws s3 cp - "$fname_out"
  done
done
