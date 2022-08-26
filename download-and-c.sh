INPUT=($1)
FNAME="${INPUT[0]}"
SHM=shm-"${INPUT[1]}"
N_BUCKETS=$2

echo "Processing $FNAME on $SHM"
aws s3 cp s3://prjna729801/"$FNAME" - \
    | gunzip \
    | sed 's/GGGGGGG*$//' \
    | ~/kmer-egd/count-kmer-eqs "$SHM" "$N_BUCKETS" \
    > /dev/null                   
