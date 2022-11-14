METADATA="rothman.unenriched.simple"
for day in {00..20}; do
    ACCESSION=$(cat $METADATA | \
                    grep HTP$ | \
                    cat -n | \
                    awk '$1-1=='$day'{print $2}')
    echo $day $ACCESSION

    (aws s3 cp s3://prjna729801/${ACCESSION}_1.fastq.gz - | \
         gunzip | \
        ./extract-reads-matching-spike-kmers.py $day 1 && \
     aws s3 cp s3://prjna729801/${ACCESSION}_2.fastq.gz - | \
         gunzip | \
         ./extract-reads-matching-spike-kmers.py $day 2) &
done
wait
