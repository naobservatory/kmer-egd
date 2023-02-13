#!/usr/bin/env bash

mkdir 2023-02-13--count-read-distribution/
cat longest-timeseries.tsv | \
    awk '{print $1}' | \
    xargs -I {} -P 32 bash -c \
      "aws s3 cp s3://prjna729801/{}.arclean.fastq.gz - | gunzip | \
         ./2023-02-13--count-read-distribution.py > \
              2023-02-13--count-read-distribution/{}.distribution.json"
