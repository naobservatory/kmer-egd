import sys
import json
import random
from collections import defaultdict
from Bio.SeqIO.FastaIO import SimpleFastaParser

K = 40

qualities_choices = ['F', ':', ',', '#']
numeric_qualities = [10**(-.1*(ord(x)-33)) for x in qualities_choices]

def simulate_error(base, quality_weights):
    chance_incorrect, = random.choices(
        numeric_qualities, weights=quality_weights, k=1)
    if random.random() > chance_incorrect:
        return base
    return random.choice(list(set('ACTG')-set(base)))

def start(genome_fname, qualities_fname, *read_counts):
    read_counts = [int(x) for x in read_counts]
    n_days = len(read_counts)

    pos_quality_weights = []
    with open(qualities_fname) as inf:
        for line in inf:
            quality = json.loads(line.strip())
            pos_quality_weights.append(
                [quality.get(x, 0) for x in qualities_choices])
    read_length = len(pos_quality_weights)

    # Make the output deterministic
    random.seed(hash(tuple(read_counts)))

    with open(genome_fname) as inf:
        (_, sequence), = SimpleFastaParser(inf)

    # kmer -> [day_1_count, day_2_count, ...]
    kmers = defaultdict(lambda : [0]*n_days)
    for n_day, read_count in enumerate(read_counts):
        for i in range(read_count):
            read_pos = random.randint(0, len(sequence) - read_length)
            read = sequence[read_pos : read_pos+read_length]
            
            errored_read = ''.join([
                simulate_error(base, quality_weights)
                for (base, quality_weights)
                in zip(read, pos_quality_weights)])
            
            for i in range(len(read) - K):
                kmers[errored_read[i:i+K]][n_day] += 1

    for kmer, counts in sorted(kmers.items()):
        print("%s\t%s" % (
            kmer, "\t".join([str(count) for count in counts])))

if __name__ == "__main__":
    start(*sys.argv[1:])
