aws s3 cp s3://prjna729801/$1 - | \
    gunzip | \
    awk '$2>0.9{print}' | \
    tail -n 100
