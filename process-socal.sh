#!/bin/bash

# Total memory ~256GB, but apparently 124GB is the most we can use
N_BYTES=130386585560

SHM=shm

N_DAYS=14
N_MODS=1
MOD=0

./close-shm $SHM > /dev/null || true
./open-shm $SHM $N_BYTES

time cat prjna729801.fnames | \
    xargs -P 32 -I {} ./download-and-c.sh {} $N_BYTES $SHM $N_DAYS $N_MODS $MOD
