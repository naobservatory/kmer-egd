#!/usr/bin/env bash

mkdir 2023-02-13--count-read-prefixes/
cat longest-timeseries.tsv | \
    awk '{print $1"_1";print $1"_2"}' | \
    xargs -I {} -P 32 bash -c \
      "aws s3 cp s3://prjna729801/{}.fastq.gz - | gunzip | \
         ./2023-02-13--count-read-prefixes.py > \
              2023-02-13--count-read-prefixes/{}.prefixes.json"
