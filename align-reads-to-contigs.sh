for day in {00..20}; do
    for reads_fname in clean-HTP-spike-reads.$day.*; do
        out=${reads_fname}.aligned.fasta
        if [ -e $out ]; then
            continue
        fi

        contig_fname=${reads_fname/reads/contigs}
        if [ ! -e $contig_fname ]; then
           continue
        fi
        
        contig=$(head -n 1 $contig_fname | awk '{print $NF}')

        echo ../sequence_tools/n2-align.py $reads_fname $out $contig
    done
done | xargs -P 8 -I {} bash -c {}
