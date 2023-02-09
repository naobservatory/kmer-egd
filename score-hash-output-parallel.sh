aws s3 ls s3://prjna729801/ | \
    awk '{print $NF}' | \
    grep ^..-hcu-40-14.tsv.gz$ | \
    xargs -P 32 -I {} ./score-hash-output-single.sh {}
