METADATA="rothman.unenriched.simple"
for day in {00..20}; do
    prefix=clean-HTP-spike-reads.$day
    if ls $prefix.* &> /dev/null; then
        continue
    fi

    if ! ls ${prefix/reads/contigs}.* &> /dev/null; then
        echo "no contigs for day $day"
        continue
    fi

    ACCESSION=$(cat $METADATA | \
                    grep HTP$ | \
                    cat -n | \
                    awk '$1-1=='$day'{print $2}')

    aws s3 cp s3://prjna729801/${ACCESSION}.arclean.fastq.gz - | \
        gunzip | \
        ./extract-reads-matching-spike-kmers.py $day &
done
wait
