#!/usr/bin/env bash

METADATA=longest-timeseries-with-lengths.tsv
OUT="longest-timeseries-tbrv.tsv"
SLUG=tbrv
cat $METADATA | while read accession date wtp total_reads; do
    echo $accession $date $wtp $total_reads \
         $(aws s3 cp s3://prjna729801/SRR14530892.$SLUG.fasta.gz - | \
               gunzip | \
               grep -c "^>")
done | tr ' ' '\t' > $OUT
