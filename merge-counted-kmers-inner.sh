FINISHED=$(
    aws s3 ls s3://prjna729801/ | \
        awk '$3>1000000{print $NF}' | \
        grep '^SRR[0-9]*_[12].fastq.gz.counted_kmers.gz$' | \
        grep -o '^[^.]*')

for slug in $@; do
    if ! [[ "$FINISHED" =~ "$slug" ]]; then
        echo "Still missing $slug" >&2
        exit
    fi
done

FNAME=$(echo $@ | \
           sed 's/SRR14530//g' | \
           tr ' ' '\n' | \
           sed 's/_.*//g' | \
           sort | uniq | \
           tr '\n' '-' | \
           sed 's/-$//' 
    ).counted_kmers.gz

if aws s3 ls s3://prjna729801/ | \
        awk '$3>80000000{print $NF}' | \
        grep "^$FNAME" > /dev/null; then
    echo "$FNAME already done, skipping" >&2
    exit
fi

CMD=$(
  echo -n 'python3 merge-counted-kmers.py'
  for slug in $@; do
    fname="$slug.fastq.gz.counted_kmers.gz"
    echo -n " <(aws s3 cp s3://prjna729801/$fname - | gunzip)"
  done

  echo " | gzip | aws s3 cp - s3://prjna729801/$FNAME"
)

echo "$CMD"

# ./merge-counts.sh > tmp.merge-counts.sh && bash tmp.merge-counts.sh
