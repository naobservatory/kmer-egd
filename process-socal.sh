#!/bin/bash

N_BUCKETS=80000000

cat prjna729801.fnames | cat -n | \
    while read n fname ; do
        echo $fname $(expr $n % 18)
    done  > prjna729801.fnames.partitioned

for i in {0..17}; do
    ./close-shm shm-$i
    ./open-shm shm-$i $N_BUCKETS
done

time cat prjna729801.fnames.partitioned | \
    xargs -P 32 -I {} ./download-and-c.sh {} $N_BUCKETS
