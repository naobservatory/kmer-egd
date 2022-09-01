N="$1"
aws s3 ls s3://prjna729801/ | \
    awk '{print $NF}' | \
    grep ^SRR | \
    grep .fastq.gz$ | \
    head -n "$N" | \
    xargs -I {} bash -c "echo {} \$(cat /proc/meminfo | grep MemAvailable) >&2 ; aws s3 cp s3://prjna729801/{} - | gunzip"
    
