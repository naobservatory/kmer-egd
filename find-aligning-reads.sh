#!/usr/bin/env bash

set -e

cat rothman.unenriched.simple | \
    awk -F '\t' '$NF=="HTP"{print $1"_1"; print $1"_2"}' | \
    xargs -P 8 -I {} bash -c "aws s3 cp s3://prjna729801/{}.fastq.gz - | \
        gunzip | \
        sed s/CTGTCTCTTATACACATCT.*// | \
        ./find-aligning-reads.py NODE_82_length_6360_cov_146981.720834.seq > \
        {}.tbrv.alignment-points"
