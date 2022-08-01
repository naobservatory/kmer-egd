args=($1)
day=${args[0]}
fastq=${args[1]}

buckets="$2"

echo "Processing $fastq for $day..."
aws s3 cp s3://prjeb29065/"$fastq" - \
    | gunzip \
    | ~/kmer-egd/count-kmer-eqs "shm-$day" "$buckets"
