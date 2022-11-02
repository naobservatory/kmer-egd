PARSED_METADATA=~/wastewater_viromics_sarscov2/metadata/parsed_metadata.tsv

for day in {00..20}; do
    ACCESSION=$(cat $PARSED_METADATA | \
                    grep HTP | \
                    grep 0$ | \
                    grep _1 | \
                    awk -F_ '{print $1}' | \
                    cat -n | \
                    awk '$1=='$day'+1{print $2}')
    aws s3 cp s3://prjna729801/${ACCESSION}_1.fastq.gz - | \
        gunzip | \
        python3 count-spike-pcr-duplicates.py \
                <(cat hc-HTP*.spikes.$day | \
                      grep ^65535 | \
                      awk '{print $NF}') > \
                hc-HTP-$day-1.pcr_duplicate_count &
done
wait  # this is dumb, but we need to not overload the server

for day in {00..20}; do
    ACCESSION=$(cat $PARSED_METADATA | \
                    grep HTP | \
                    grep 0$ | \
                    grep _1 | \
                    awk -F_ '{print $1}' | \
                    cat -n | \
                    awk '$1=='$day'+1{print $2}')
    aws s3 cp s3://prjna729801/${ACCESSION}_2.fastq.gz - | \
        gunzip | \
        python3 count-spike-pcr-duplicates.py \
                <(cat hc-HTP*.spikes.$day | \
                      grep ^65535 | \
                      awk '{print $NF}') > \
                hc-HTP-$day-2.pcr_duplicate_count &

done
wait
