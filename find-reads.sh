KMER="$1"
cat prjna729801.fnames | xargs -P 32 -I {} ./find-reads-single.sh {} $KMER
