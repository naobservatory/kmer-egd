METADATA=~/wastewater_viromics_sarscov2/metadata/parsed_metadata.tsv
for day in {00..20}; do
    ACCESSION=$(cat $METADATA | \
                    grep HTP | \
                    grep 0$ | \
                    grep _1 | \
                    cat -n | \
                    awk '{printf("%02d\t%s\n", $1-1, $2)}' | \
                    grep ^$day | \
                    awk '{print $2}' | \
                    awk -F_ '{print $1}')

    (aws s3 cp s3://prjna729801/${ACCESSION}_1.fastq.gz - | \
        gunzip | \
        python3 extract-reads-matching-spike-kmers.py $day 1 && \
     aws s3 cp s3://prjna729801/${ACCESSION}_2.fastq.gz - | \
         gunzip | \
         python3 extract-reads-matching-spike-kmers.py $day 2) &
done
wait
