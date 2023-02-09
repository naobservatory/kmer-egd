for accession in $(cat rothman.unenriched.simple | \
       awk -F '\t' '$3=="HTP"{print $1}'); do
    aws s3 cp s3://prjna729801/${accession}_1.fastq.gz - | \
        gunzip | grep '^[ACGT]' | \
        sed 's/CTGTCTCTTATACACATCT.*//' | \
        awk '{print length($1)}' | sort -n | uniq -c > \
           $accession.dumb.insert-lengths
done
