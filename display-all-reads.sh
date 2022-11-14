for day in {00..20}; do
    for in_f in hc-HTP-spike-reads.$day.*.aligned.fasta; do
        if [ ! -e $in_f ]; then
            continue;
        fi

        out=${in_f/.aligned.fasta/.display}
        if [ -e $out ]; then
            continue;
        fi

        echo $in_f

        bare=${in_f/.aligned.fasta}
        contig=$(head -n 1 ${bare/reads/contigs} | awk '{print $NF}')
        cat $in_f | \
            sed s/CTGTCTCTTATACACATCT.*// | \
            sed s/GGGGGGGG*$// | \
            ~/code/sequencing_tools/display-reads.py $contig | \
            ~/code/sequencing_tools/color-mismatches.py > $out
    done
done
