FNAME=$1
N_BYTES=$2
SHM=$3
N_DAYS=$4
N_MODS=$5
MOD=$6

echo "Processing $FNAME $MOD/$N_MODS on $SHM with $N_DAYS simulated days"
aws s3 cp s3://prjna729801/"$FNAME" - \
    | gunzip \
    | sed 's/GGGGGGGG*$//' \
    | ~/kmer-egd/count-kmer-eqs $N_BYTES $SHM $N_DAYS $N_MODS $MOD
