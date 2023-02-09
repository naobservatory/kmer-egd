aws s3 ls s3://prjna729801/ | \
    awk '{print $NF}' | \
    grep '^SRR[0-9]*_[12].fastq.gz$' | \
    sed 's/[.].*//' | \
    xargs -P 1 -L 4 bash merge-counted-kmers-inner.sh | \
    grep -v 738-739.counted_kmers.gz | \
    parallel -P 8

#aws s3 ls s3://prjna729801/ | \
#    awk '$3>1000000{print $NF}' | \
#    grep '^SRR[0-9]*_[12].fastq.gz.counted_kmers.gz$' | \
#    grep -o '^[^.]*' | \
#    xargs -P 1 -L 8 bash merge-counted-kmers-inner.sh
