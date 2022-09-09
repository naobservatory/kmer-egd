cat $1 | \
    python3 eval-buckets-sm.py | \
    sort -t$'\t' -k 4 -g | \
    head -n 1 > \
         $1.top
