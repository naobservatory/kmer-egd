#!/usr/bin/env bash

SEQ=pmmov.seq
METADATA=longest-timeseries.tsv
SLUG=pmmov

mkdir $SLUG

for accession in $(cat $METADATA | awk '{print $1}'); do
    aws s3 cp s3://prjna729801/${accession}.arclean.fastq.gz - | \
        gunzip | \
        ./extract-reads-matching-seq.py $SEQ \
           > $SLUG/$accession.fasta &
done
wait

zip -r $SLUG.zip $SLUG/
