for final in 100 200 300 400 500 600 700 800 900 1000 1100 1200 1300 1400 \
                 1500 1600 1700 1800 1900 2000; do
    echo -n $final
    for growth in 05 07 10 15; do
        echo -n "" $(python3 virtual-spike-in.py \
                                      hiv.fasta \
                                      quality-counts.jsons $(
            python3 spike-in-growth.py 14 $final .$growth) | \
                python3 eval-buckets-sm.py | \
                sort -g | \
                head -n 1 | \
                awk '{print $1}')
    done
    echo 
done | tr ' ' '\t'
