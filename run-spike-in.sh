if ! [[ -e hiv-spikes.tsv ]]; then
    python3 virtual-spike-in.py hiv.fasta quality-counts.jsons $(
        python3 spike-in-growth.py 14 1000 .15) > \
            hiv-spikes.tsv
fi

python3 fetch-kmer-counts.py hiv-spikes.tsv hiv
