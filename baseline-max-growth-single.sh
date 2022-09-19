aws s3 cp s3://prjna729801/$1 - 2>/dev/null | \
    gunzip | \
    head -n 1000
