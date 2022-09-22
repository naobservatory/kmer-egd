DAYS=$1
shift
VALS="$@"

for final in $VALS; do
    echo -n $final
    for growth in .05 .07 .10 .15; do
        echo -n "" $(python3 virtual-spike-in.py \
                                      hiv.fasta \
                                      quality-counts.jsons $(
            python3 spike-in-growth.py $DAYS $final $growth) | \
                python3 eval-buckets-sm.py | \
                sort -g | \
                head -n 1 | \
                awk '{print $1}')
    done
    echo 
done | tr ' ' '\t'
