# This is pretty silly: we want to use ./fasta-to-kmers to tell us which
# specific lines to extract.  This could be way more efficient, but this is
# probably good enough.
aws s3 cp s3://prjna729801/EC-40-14-2B.tsv.gz - | \
    gunzip | \
    grep -E $(cat hiv.fasta | \
                  ./fasta-to-ecs 2328331885 | \
                  awk '{print $2}' | \
                  sort -n | \
                  uniq | \
                  sed 's~^~^~' | \
                  sed 's~$~\\s~' | \
                  tr '\n' '|' | \
                  sed 's/.$/\n/') > \
         hiv-ec-counts.tsv
