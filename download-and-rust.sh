aws s3 cp s3://prjna729801/"$1" - \
    | gunzip \
    | ~/kmer-egd/target/release/kmer-egd "$2" \
    > /dev/null
