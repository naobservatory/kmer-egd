#!/usr/bin/env bash

FASTA=$1
METADATA=longest-timeseries.tsv
SLUG=reads-${FASTA/.fasta/}

mkdir $SLUG

for accession in $(cat $METADATA | awk '{print $1}'); do
    aws s3 cp s3://prjna729801/${accession}.arclean.fastq.gz - | \
        gunzip | \
        ./extract-reads-matching-seq.py $FASTA \
           > $SLUG/$accession.fasta &
done
wait

zip -r $SLUG.zip $SLUG/
rm -r $SLUG/
