for a in A C G T; do
    for b in A C G T; do
        for c in A C G T; do
            for d in A C G T; do
                PREFIX="${a}${b}${c}${d}"
                INCLUDE="${PREFIX}AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
                EXCLUDE="${PREFIX}ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"
                echo "$PREFIX"
                echo "$PREFIX" >&2
                time ./cat-n-socal.sh 360 | \
                    ~/kmer-egd/trie-count "$INCLUDE" "$EXCLUDE" | \
                    gzip | \
                    aws s3 cp - "s3://prjna729801/$PREFIX-40-14.tsv.gz"
            done;
        done;
    done;
done 2> 40-14.log
