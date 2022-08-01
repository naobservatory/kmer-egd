# 17 buckets at 1B entries each (4GB each) is 68GB, and we have ~120GB.  This
# doesn't work, trying just 100M entries each for now.
buckets=100000000

for day in {1..17}; do
    ./open-shm "shm-$day" "$buckets"
done

cat ~/PRJEB29065/diet-days.txt | \
    xargs -P 28 -I {} ./process-diet-single.sh {} "$buckets"
