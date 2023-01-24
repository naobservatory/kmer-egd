#!/usr/bin/bash

SEQ=tomato.brown.rugose.nt.seq
METADATA=longest-timeseries.tsv
SLUG=tbrv

for accession in $(cat $METADATA | awk '{print $1}'); do
    aws s3 cp s3://prjna729801/${accession}.arclean.fastq.gz - | \
        gunzip | \
        ./extract-reads-matching-seq.py $SEQ \
           > $SLUG.$accession.fasta &
done
wait
