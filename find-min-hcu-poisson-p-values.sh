aws s3 ls s3://prjna729801/ | \
    grep hcu.*poisson | \
    awk '{print $NF}' | \
    xargs -P 32 -I {} bash -c \
"aws s3 cp s3://prjna729801/{} - | \
gunzip | \
awk '{print $1}' | \
sort -g | \
head -n 100 > \
{}.min-p"
