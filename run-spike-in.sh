if ! [[ -e spikes.tsv ]]; then
    python3 virtual-spike-in.py swine-flu.fasta quality-counts.jsons $(
        python3 spike-in-growth.py 14 1000 .15) > \
            spikes.tsv
fi

python3 fetch-kmer-counts.py spikes.tsv swine
