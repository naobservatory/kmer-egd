#!/usr/bin/env bash

SEQUENCE_FILE="$1"

for a in A C G T; do
    for b in A C G T; do
        prefix=$a$b
        fname_in="s3://prjna729801/clean-HTP-$prefix.gz"

        echo $prefix
        aws s3 cp "$fname_in" - | \
            gunzip | \
            ./extract-kmer-counts.py "$prefix" "$SEQUENCE_FILE" \
                    > "$SEQUENCE_FILE.$prefix" &
    done
done
wait
         
