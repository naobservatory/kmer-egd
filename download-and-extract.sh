FNAME="$1"
shift
aws s3 cp s3://prjna729801/"$FNAME" - \
    | gunzip \
    | ~/kmer-egd/extract-kmers "$@"
