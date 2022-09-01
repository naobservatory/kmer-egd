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
        time aws s3 cp "s3://prjna729801/$fname" - | \
            gunzip | \
            python3 eval-buckets.py | \
            awk '{print $1"\t"$2"\t"$3}' | \
            sort -n | \
            gzip | \
            aws s3 cp - "s3://prjna729801/${fname/.tsv.gz/-poisson.tsv.gz}"
    fi
done
