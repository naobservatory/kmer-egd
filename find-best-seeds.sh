#!/usr/bin/env bash

# Assumes count-consistent-timeseries.sh has already run

TARGETS="tbrv.OM305070.1.fasta pmmov.ON493797.1.fasta cgmmv.NC_001801.1.fasta tmv.MH507166.1.fasta tmgmv.MZ395975.1.fasta tsamv.NC_030229.1.fasta tmmv.MW373515.1.fasta ca.KX342792.1.fasta ov2.OK428619.1.fasta mnsv.AB232926.1.fasta"

for wtp in $(cat longest-timeseries.tsv | awk '{print $3}' | sort | uniq); do
    for a in A C G T; do
        # This is subsampled, but that's not a problem.
        fname_in="s3://prjna729801/clean-TS-ss-$wtp-$a.gz"
        
        aws s3 cp "$fname_in" - | \
            gunzip | \
            ./find-best-seeds.py $TARGETS > best-seeds.$wtp.$a.tmp &
    done
done

wait
