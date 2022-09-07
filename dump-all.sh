#for i in {0..31} ; do
#  ./shm-dump-all 80000000 32 $i $(echo {0..17} | tr ' ' '\n' | sed s/^/shm-/) \
#       | python3 eval-buckets.py \
#       > bucket-evaluations-$i-of-32.tsv &
#done

#wait
