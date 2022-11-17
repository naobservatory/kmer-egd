PRIMER_1_RC=CTGTCTCTTATACACATCTCCGAGCCCACGAGAC
PRIMER_2_RC=CTGTCTCTTATACACATCTGACGCTGCCGACGA
P5_RC=GTGTAGATCTCGGTGGTCGCCGTATCATT
P7_RC=ATCTCGTATGCCGTCTTCTGCTTG
for day in {00..20} ; do
    prefix=hc-HTP-spike-contigs.$day
    i5=$(cat rothman-htp-barcodes | awk '$1=='$day'{print $3}')
    i7=$(cat rothman-htp-barcodes | awk '$1=='$day'{print $2}')

    P5_adapter=$PRIMER_1_RC$i5$P5_RC
    P7_adapter=$PRIMER_2_RC$i7$P7_RC

    ./remove-adapter-spikes.py \
        $prefix $P5_adapter $P7_adapter
done
