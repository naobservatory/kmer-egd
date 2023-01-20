#!/usr/bin/env bash

METADATA=longest-timeseries.tsv
OUT="longest-timeseries-tbrv.tsv"
SLUG=tbrv

cat $METADATA | while read accession date wtp; do
    echo $accession $date $wtp \
         $(cat all.$accession.count) \
         $(cat $SLUG.$accession.count)
done | tr ' ' '\t' > $OUT
