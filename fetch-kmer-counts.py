import os
import sys
import subprocess
from collections import defaultdict

PREFIX_LEN=4
K=40
DAYS=14

kmers_by_prefix = defaultdict(list)
existing_s3_files = set()

def start(spikes_fname, job_name):
    with open(spikes_fname) as inf:
        for line in inf:
            kmer = line.split('\t')[0]
            kmers_by_prefix[kmer[:PREFIX_LEN]].append(kmer)

    s3_raw_output = subprocess.check_output(
        ["aws", "s3", "ls", "s3://prjna729801/"])
    for record in s3_raw_output.decode('utf-8').split('\n'):
        if not record.strip(): continue
        existing_s3_files.add(record.split()[-1])
            
    for prefix, kmers in kmers_by_prefix.items():
        trie_output_fname = "%s-%s-%s.tsv.gz" % (prefix, K, DAYS)
        kmer_count_fname = "%s-%s-%s-%s.tsv" % (job_name, prefix, K, DAYS)
        if (trie_output_fname in existing_s3_files and
            not os.path.exists(kmer_count_fname)):

            print("Extracting %s kmers from %s and writing to %s..." % (
                len(kmers), trie_output_fname, kmer_count_fname))

            subprocess.check_call(
                "aws s3 cp s3://prjna729801/%s-%s-%s.tsv.gz - | "
                "gunzip | "
                "grep '%s' > %s || echo '%s: no matching kmers'" % (
                    prefix, K, DAYS,
                    "\\|".join('^%s' % kmer for kmer in kmers),
                    kmer_count_fname, prefix), shell=True)

if __name__ == "__main__":
    start(*sys.argv[1:])
