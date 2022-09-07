FNAME=$1
KMER=$2

aws s3 cp s3://prjna729801/$FNAME - | \
    gunzip | \
    fgrep -B 1 $KMER
