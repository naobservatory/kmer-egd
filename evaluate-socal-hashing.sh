#for a in A C G T; do
#    for b in A C G T; do
#        for c in A C G T; do
#            for d in A C G T; do
#                PREFIX="${a}${b}${c}${d}"
for PREFIX in AA; do
                INCLUDE="${PREFIX}AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
                EXCLUDE="${PREFIX}ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"
                echo "$PREFIX HU x4"
                echo "$PREFIX HU x4" >&2
                time ./cat-n-socal.sh 360 | \
                    ~/kmer-egd/hash-count-union "$INCLUDE" "$EXCLUDE"

        #| \
        #            gzip | \
        #            aws s3 cp - "s3://prjna729801/$PREFIX-hashu-40-14.tsv.gz"
#            done;
#        done;
#    done;
done 2> hash-eval-40-14.log
