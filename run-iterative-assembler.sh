#!/usr/bin/env bash

# Assumes find-best-seeds.sh has already run

./iterative-assembler.sh \
    best-seeds.tsv \
    $(cat longest-timeseries.tsv | awk '{print $1}')
