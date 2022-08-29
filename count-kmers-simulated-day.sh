echo "Starting $1"
aws s3 cp s3://prjna729801/$1 - | \
    gunzip | \
    python3 print-kmer-simulated-day.py | \
    grep -v 'GGGGGGGG$' | \
    sort | \
    uniq -c | \
    awk '{print $2"\t"$1}' | \
    gzip | \
    aws s3 cp - s3://prjna729801/$1.counted_kmers.gz
