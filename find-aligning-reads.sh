#!/usr/bin/env bash

set -e

for accession in $(cat rothman.unenriched.simple | \
                       awk -F '\t' '$NF=="HTP"{print $1}'); do
    aws s3 cp s3://prjna729801/$accession.arclean.fastq.gz - | \
        gunzip | \
        ./find-aligning-reads.py NODE_82_length_6360_cov_146981.720834.seq > \
                                 $accession.tbrv.alignment-points &
done
wait
