ls hiv-spikes-* | xargs -P 32 -I {} ./process-hiv-spikes-single.sh {}
for final in $(seq 1000 1000 15000); do
    for rate in 05 10 15 ; do
        echo -e "$final\t$rate%\t$(cat hiv-spikes-$final-$rate.tsv.top)"
    done
done

