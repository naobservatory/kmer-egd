#!/usr/bin/env bash

set -e

adapter_trimming=../wastewater_viromics_sarscov2/adapter_trimming
determine_adapter=${adapter_trimming}/determine_adapter.py
for accession in $(cat rothman.unenriched.simple | \
                       awk -F '\t' '$NF=="HTP"{print $1}'); do
    in1="${accession}_1.fastq.gz"
    in2="${accession}_2.fastq.gz"
    aws s3 cp s3://prjna729801/$in1 .
    aws s3 cp s3://prjna729801/$in2 .

    AdapterRemoval \
        --file1 $in1 \
        --file2 $in2 \
        --basename $accession \
        --trimns \
        --trimqualities \
        --collapse \
        --interleaved-output \
        --adapter1 $(cat $in1 | gunzip | $determine_adapter - fwd) \
        --adapter2 $(cat $in2 | gunzip | $determine_adapter - rev)

    collapsed=${accession}.collapsed
    collapsed_truncated=${accession}.collapsed.truncated
    discarded=${accession}.discarded
    paired=${accession}.paired.truncated
    singleton_truncated=${accession}.singleton.truncated

    out_nogz=${accession}.arclean.fastq
    out=${out_nogz}.gz

    cat $collapsed $collapsed_truncated $paired $singleton_truncated > \
        $out_nogz
    gzip $out_nogz

    aws s3 cp $out s3://prjna729801/$out

    rm $in1 $in2 $collapsed $collapsed_truncated $discarded \
       $paired $singleton_truncated $out

done
