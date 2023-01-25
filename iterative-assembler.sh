#!/usr/bin/bash

# A greedy assembler that assembles a single contig from a large amount of data
# given a seed.
#
# 1. The contig starts as the seed.
# 2. Extract all reads that overlap with the current contig.
# 3. Extend the current contig by finding the most common value at each
#    position.
#
# This is lazy in several ways, including that it doesn't attempt to handle
# read errors or variation.  It just steamrolls ahead with the most common
# variant at every point.

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

WORKDIR=$1
shift
SEED=$1
shift
ACCESSIONS="$@"

mkdir "$WORKDIR"
cd "$WORKDIR"

CONTIG=$SEED
ITERATION=0
while true; do
    ITERATION=$(($ITERATION + 1))
    echo $CONTIG > $ITERATION.contig.seq
    echo $ACCESSIONS | \
        tr ' ' '\n' | \
        xargs -P 32 -I {} bash -c \
            "aws s3 cp s3://prjna729801/{}.arclean.fastq.gz - | \
             gunzip | \
             $SCRIPT_DIR/extract-overlapping-reads.py {} $CONTIG > \
             {}.$ITERATION.fasta"
      
    CONTIG=$($SCRIPT_DIR/iterative-assembler.py $ITERATION $CONTIG)
    if [ $? -eq 42 ]; then
        echo $CONTIG > final_contig.seq
        break
    fi
done
