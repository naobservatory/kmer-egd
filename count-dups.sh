#!/usr/bin/env bash

for accession in $(cat rothman.unenriched.simple | \
                       awk -F '\t' '$NF=="HTP"{print $1}'); do
    aws s3 cp s3://prjna729801/$accession.arclean.fastq.gz - | \
        gunzip | \
        grep -E -o '^[ACGT]{50}' | \
        sort | uniq -c | sort -n | \
        awk '{print $1}' | sort -n | uniq -c > $accession.dup-counts
done

cat rothman.unenriched.simple | \
    while read accession date wtp ; do \
        if [ ! -e $accession.dup-counts ] ; then continue ; fi
        echo $date $accession $(\
          cat $accession.dup-counts | \
             awk '$2==1{ones=$1}\
                 {total+=($1*$2)}\
                 END{print(1-(ones/total))*100"%", (total-ones)"/"total}')
    done
