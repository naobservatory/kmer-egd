for day in {00..20}; do
    for reads_fname in hc-HTP-spike-reads.$day.c.*; do
        out=${reads_fname/.c./.}.aligned.fasta
        if [ -e $out ]; then
            continue
        fi

        contig_fname=${reads_fname/reads.$day.c/contigs.$day}
        if [ ! -e $contig_fname ]; then
           continue
        fi
        
        contig=$(head -n 1 $contig_fname | awk '{print $NF}')

        echo ~/code/sequencing_tools/n2-align.py \
             $reads_fname \
             ${reads_fname/.c./.}.aligned.fasta \
             $contig
    done
done | xargs -P 8 -I {} bash -c {}
