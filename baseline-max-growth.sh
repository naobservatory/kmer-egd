aws s3 ls s3://prjna729801 | \
    awk '{print $NF}' | \
    grep poisson | grep -v EC- | \
    xargs -P 32 -I {} ./baseline-max-growth-single.sh {} | \
    sort -n | \
    grep ^0.000000
