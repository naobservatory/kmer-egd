for i in {0..31} ; do
    cat bucket-evaluations-$i-of-32.tsv \
        | grep -v '^\[' \
        | sort -g \
               > bucket-evaluations-$i-of-32.sorted.tsv &
done
wait
