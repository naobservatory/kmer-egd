WTP="$1"
for a in A C G T; do
    for b in A C G T; do
        time cat rothman.unenriched.simple | \
            awk -F '\t' '$NF=="'$WTP'"{print $1"_1.fastq.gz\n"$1"_2.fastq.gz"}' | \
            xargs -P1 -I {} aws s3 cp s3://prjna729801/{} - | \
            gunzip | \
            ./hash-count-rothman $WTP $a$b | \
            gzip | \
            aws s3 cp - s3://prjna729801/hc-$WTP-$a$b.gz
    done
done
