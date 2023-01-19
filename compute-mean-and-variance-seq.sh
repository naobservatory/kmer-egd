#!/bin/bash

SEQUENCE_FILE="$1"

for wtp in $(cat longest-timeseries.tsv | awk '{print $3}' | sort | uniq); do
    for a in A C G T; do
        cat "$SEQUENCE_FILE.$wtp.$a" | \
            ./compute-mean-and-variance.py \
                > "$SEQUENCE_FILE.$wtp.$a.mvl"
    done
done

for wtp in $(cat longest-timeseries.tsv | awk '{print $3}' | sort | uniq); do
    cat "$SEQUENCE_FILE.$wtp.A.mvl" \
        "$SEQUENCE_FILE.$wtp.C.mvl" \
        "$SEQUENCE_FILE.$wtp.G.mvl" \
        "$SEQUENCE_FILE.$wtp.T.mvl" | \
        ./merge-per-prefix-counts.py \
            > "$SEQUENCE_FILE.$wtp.uniq-c.mvl"
done
