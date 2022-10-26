for a in A C G T; do
    for b in A C T G; do
        echo $a$b
        aws s3 cp s3://prjna729801/hc-HTP-$a$b.gz - |\
            gunzip | \
            python3 summarize-wtp.py > \
                   hc-HTP-$a$b.summary &
    done
done
