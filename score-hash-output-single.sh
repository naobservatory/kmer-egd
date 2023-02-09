fname=$1
time aws s3 cp "s3://prjna729801/$fname" - | \
    gunzip | \
    python3 eval-buckets-sm.py | \
    gzip | \
    aws s3 cp - "s3://prjna729801/${fname/.tsv.gz/-poisson.tsv.gz}"
