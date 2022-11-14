ADAPTER=CTGTCTCTTATACACATCT
for day in {00..20} ; do
    prefix=hc-HTP-spike-contigs.$day
    fwd_bc=$(cat rothman-htp-barcodes | awk '$1=='$day'{print $2}')
    rev_bc=$(cat rothman-htp-barcodes | awk '$1=='$day'{print $3}')
    ./remove-adapter-spikes.py $prefix $ADAPTER $fwd_bc $rev_bc
done
