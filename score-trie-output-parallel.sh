aws s3 ls s3://prjna729801/ | \
    awk '{print $NF}' | \
    grep ^....-40-14.tsv.gz$ | \
    xargs -P 8 -I {} ./score-trie-output-single.sh {}
