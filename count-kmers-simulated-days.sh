cat prjna729801.fnames | \
    xargs -P 4 -I {} ./count-kmers-simulated-day.sh {}

