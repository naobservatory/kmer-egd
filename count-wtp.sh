for a in A C G T; do
    for b in A C G T; do
        fname_out="s3://prjna729801/hc-HTP-$a$b.gz"

        if aws s3 ls "$fname_out" > /dev/null ; then
            continue
        fi

        echo "... $a$b"
        time cat rothman.unenriched.simple | \
            awk -F '\t' '$NF=="HTP"{print $1"_1.fastq.gz\n"$1"_2.fastq.gz"}' | \
            xargs -P1 -I {} aws s3 cp s3://prjna729801/{} - | \
            gunzip | \
            ./hash-count-rothman HTP $a$b | \
            gzip | \
            aws s3 cp - "$fname_out"
    done
done
