for day in {00..20}; do
    fname_out="s3://prjna729801/clean-HTP.spikes.$day.gz"

    if aws s3 ls "$fname_out" > /dev/null ; then
        continue
    fi

    echo "$day..."

    for a in A C G T ; do
        for b in A C G T ; do
            aws s3 cp s3://prjna729801/clean-HTP-$a$b.spikes.gz - | gunzip
        done
    done | \
        python3 partition-spikes.py $day | \
        gzip | \
        aws s3 cp - $fname_out
done
