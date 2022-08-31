echo -n 'python3 merge-counts.py'

aws s3 ls s3://prjna729801/ | \
    grep counted_kmers.gz | \
    awk '$3>1000000{print $NF}' | \
    while read fname; do
        echo -n " <(aws s3 cp s3://prjna729801/$fname - | gunzip)"
    done
echo
# ./merge-counts.sh > tmp.merge-counts.sh && bash tmp.merge-counts.sh
