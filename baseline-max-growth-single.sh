aws s3 cp s3://prjna729801/$1 - | \
    gunzip | \
    tail -n 100
