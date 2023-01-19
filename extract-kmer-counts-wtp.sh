#!/usr/bin/env bash

SEQUENCE_FILE="$1"

for wtp in HTP OC SJ JWPCP; do
    for a in A C G T; do
        fname_in="s3://prjna729801/clean-TS-ss-$wtp-$a.gz"

        echo $a
        aws s3 cp "$fname_in" - | \
            gunzip | \
            ./extract-kmer-counts.py "$a" "$SEQUENCE_FILE" \
                    > "$SEQUENCE_FILE.$wtp.$a" &
    done
done
wait
