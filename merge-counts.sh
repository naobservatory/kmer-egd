echo -n 'python3 merge-counts.py'

cat prjna729801.fnames | while read fname; do
    echo -n " <(aws s3 cp s3://prjna729801/$fname.counted_kmers.gz - | gunzip)"
done

# ./merge-counts.sh > tmp.merge-counts.sh && bash tmp.merge-counts.sh
