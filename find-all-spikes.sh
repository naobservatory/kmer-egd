for a in A C G T; do
    for b in A C G T; do
        echo $a$b
        aws s3 cp s3://prjna729801/hc-HTP-$a$b.gz - | \
            gunzip | \
            python3 find-spikes.py | \
            gzip | \
            aws s3 cp - s3://prjna729801/hc-HTP-$a$b.spikes.gz &
    done
done
wait
         
