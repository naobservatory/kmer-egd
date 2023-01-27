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
#
# Since the main cost is the corpus scans, assemble multiple contigs in
# parallel.

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

SEEDS=$(realpath $1)
shift
ACCESSIONS="$@"

mkdir iterative-assembly
cd iterative-assembly

cat $SEEDS | sed s/.fasta// | while read target count seed; do
    if [ ! -e $target ]; then
        mkdir $target
        echo $seed > $target/0.contig.seq
    fi
done

TARGETS=$(cat $SEEDS | sed 's/.fasta.*//')

while true; do
    echo "Scanning..."
    echo $ACCESSIONS | \
        tr ' ' '\n' | \
        xargs -P 32 -I {} bash -c \
            "aws s3 cp s3://prjna729801/{}.arclean.fastq.gz - | \
             gunzip | \
             $SCRIPT_DIR/extract-overlapping-reads.py {} $SEEDS"
    
    should_stop=true
    for target in $TARGETS; do
        if [ ! -e $target/final_contig.seq ]; then
            should_stop=false
            $SCRIPT_DIR/iterative-assembler.py $target &
        fi
    done
    if $should_stop; then
        break  # we stop once every sequence has finished
    else
        echo "Assembling..."
    fi
    wait
done
