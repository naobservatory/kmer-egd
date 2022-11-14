ADAPTER=CTGTCTCTTATACACATCT
for day in {00..20} ; do
    prefix=hc-HTP-spike-contigs.$day
    ./remove-adapter-spikes.py $prefix $ADAPTER
done
