WTP="$1"
for a in A C G T; do
    for b in A C G T; do
        echo $WTP $a $b
        time aws s3 cp s3://prjna729801/hc-$WTP-$a$b.gz - | \
            gunzip | \
            python3 eval-buckets-sm.py HTP \
              ~/wastewater_viromics_sarscov2/metadata/parsed_metadata.tsv | \
            gzip | \
            aws s3 cp - s3://prjna729801/hc-$WTP-$a$b.poisson.gz &
    done
done
wait
