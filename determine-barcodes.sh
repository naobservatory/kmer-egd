PRE_A="CTGTCTCTTATACACATCTCCGAGCCCACGAGAC"
PRE_B="CTGTCTCTTATACACATCTGACGCTGCCGACGA"
POST_A="ATCTCGTATGCCGTCTTCTGCTTGAAAAGGG"
POST_B="GTGTAGATCTCGGTGGTCGCCGTATCATTAAA"

echo -e "day\tbc_a\tbc_b\ta_f\ta_r\tb_f\tb_r"
for day in {00..20} ; do
    ACCESSION=$(
        cat ~/wastewater_viromics_sarscov2/metadata/parsed_metadata.tsv | \
            grep HTP | grep 0$ | grep _1 | cat -n | \
            awk '{printf("%02d\t%s\n", $1-1, $2)}' | \
            grep ^$day | \
            awk '{print $2}' | \
            awk -F_ '{print $1}')
    
    BC_A=$(aws s3 cp s3://prjna729801/${ACCESSION}_1.fastq.gz - | \
               gunzip | \
               grep -E "$PRE_A[ACTG]{10}$POST_A" | \
               sed "s/.*$PRE_A//" | \
               sed "s/$POST_A.*//" | \
               sort | uniq -c | sort -n | \
               tail -n 1 | \
               awk '{print $NF}')    
    BC_B=$(aws s3 cp s3://prjna729801/${ACCESSION}_2.fastq.gz - | \
               gunzip | \
               grep -E "$PRE_B[ACTG]{10}$POST_B" | \
               sed "s/.*$PRE_B//" | \
               sed "s/$POST_B.*//" | \
               sort | uniq -c | sort -n | \
               tail -n 1 | \
               awk '{print $NF}')
               
    A_FWD=$(
        aws s3 cp s3://prjna729801/${ACCESSION}_1.fastq.gz - | \
            gunzip | \
            fgrep -c $BC_A)
    A_REV=$(
        aws s3 cp s3://prjna729801/${ACCESSION}_2.fastq.gz - | \
            gunzip | \
            fgrep -c $BC_A)

    B_FWD=$(
        aws s3 cp s3://prjna729801/${ACCESSION}_1.fastq.gz - | \
            gunzip | \
            fgrep -c $BC_B)
    B_REV=$(
        aws s3 cp s3://prjna729801/${ACCESSION}_2.fastq.gz - | \
            gunzip | \
            fgrep -c $BC_B)

    COUNTS="$A_FWD\t$A_REV\t$B_FWD\t$B_REV"
    echo -e "$day\t$BC_A\t$BC_B\t$COUNTS"
done
