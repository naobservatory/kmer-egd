#!/usr/bin/env bash

METADATA=longest-timeseries-with-lengths.tsv
OUT="longest-timeseries-tbrv.tsv"
SLUG=tbrv

for accession in $(cat $METADATA | awk '{print $1}'); do
    aws s3 cp s3://prjna729801/$accession.$SLUG.fasta.gz - | \
          gunzip | \
          grep -c "^>" > $SLUG.$accession.count &
    echo $accession
done

wait

cat $METADATA | while read accession date wtp total_reads; do
    echo $accession $date $wtp $total_reads \
         $(cat $SLUG.$accession.count)
done | tr ' ' '\t' > $OUT
