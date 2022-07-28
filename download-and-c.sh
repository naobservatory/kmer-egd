aws s3 cp s3://prjna729801/"$1" - \
    | gunzip \
    | ~/kmer-egd/count-kmer-eqs "$2" \
    > /dev/null                   
