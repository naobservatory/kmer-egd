#!/usr/bin/env bash

if [ ! -e rothman.unenriched.lengths.simple ]; then
    cat rothman.unenriched.simple | \
        while read accession date wtp ; do
            echo $accession $date $wtp $(
                aws s3 cp s3://prjna729801/${accession}_1.fastq.gz - \
                    2>/dev/null | \
                    gunzip | \
                    head -n 2 | \
                    tail -n 1 | \
                    wc -c)
        done | tr ' ' '\t' > rothman.unenriched.lengths.simple
fi

cat rothman.unenriched.lengths.simple | \
    ./find-best-timeseries.py > longest-timeseries.tsv
