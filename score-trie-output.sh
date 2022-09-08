READY=$(aws s3 ls s3://prjna729801/ | \
            awk '{print $NF}' | \
            grep ^....-40-14.tsv.gz$)
FINISHED=$(aws s3 ls s3://prjna729801/ | \
            awk '{print $NF}' | \
            grep ^....-40-14-poisson.tsv.gz$ | \
            sed s/-poisson//)

for fname in $READY; do
    if ! [[ "$FINISHED" =~ "$fname" ]]; then
        echo "$fname"
        ./score-trie-output-single.sh "$fname"
    fi
done
