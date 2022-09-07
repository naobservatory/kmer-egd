for i in {00..31}; do
    aws s3 cp "s3://prjna729801/EC-40-14-2B.tsv.gz" - | \
        gunzip | \
        python3 select-mod-lines.py 32 $i | \
        python3 eval-buckets.py | \
        awk '{print $1"\t"$2"\t"$3}' | \
        sort -n | \
        gzip | \
        aws s3 cp - "s3://prjna729801/EC-40-14-2B.$i.poisson.tsv.gz" &
done
wait
