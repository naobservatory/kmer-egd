for a in A C G T; do
    for b in A C G T; do
        fname_out="s3://prjna729801/clean-HTP-$a$b.gz"

        if aws s3 ls "$fname_out" > /dev/null ; then
            continue
        fi

        echo "... $a$b"
        time cat rothman.unenriched.simple | \
            awk -F '\t' '$NF=="HTP"{print $1".arclean.fastq.gz"}' | \
            xargs -P1 -I {} aws s3 cp s3://prjna729801/{} - | \
            gunzip | \
            sed -E 's/^@MT?_/@/' | \
            ./hash-count-rothman HTP $a$b | \
            gzip | \
            aws s3 cp - "$fname_out"
    done
done
