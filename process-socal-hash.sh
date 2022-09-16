for a in A C G T; do
    for b in A C G T; do
        PREFIX="${a}${b}"
        INCLUDE="${PREFIX}AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        EXCLUDE="${PREFIX}ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"
        echo "$PREFIX"
        echo "$PREFIX" >&2
        time ./cat-n-socal.sh 360 | \
            ~/kmer-egd/hash-count-union "$INCLUDE" "$EXCLUDE" | \
            gzip | \
            aws s3 cp - "s3://prjna729801/$PREFIX-hcu-40-14.tsv.gz"
    done;
done 2> hash-40-14.log
