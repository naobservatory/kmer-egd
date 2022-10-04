import sys
from collections import defaultdict
n_kmer_types_to_tokens = defaultdict(int)

total_types = 0
total_tokens = 0
with open("rothman.unenriched.counts") as inf:
    for line in inf:
        n_kmer_types, tokens_of_each = line.strip().split()
        n_kmer_types_to_tokens[int(tokens_of_each)] += int(n_kmer_types)

total_types = sum(n_kmer_types
                  for _, n_kmer_types
                  in n_kmer_types_to_tokens.items())
total_tokens = sum(n_kmer_types * tokens_of_each
                   for tokens_of_each, n_kmer_types
                   in n_kmer_types_to_tokens.items())

# Would want to iterate through the types by descending number of tokens, but
# there are too many types (9B) to literally do this.

data = [(tokens_of_each, n_kmer_types)
        for tokens_of_each, n_kmer_types
        in n_kmer_types_to_tokens.items()]
data.sort(reverse=True)

cumulative_tokens = 0
cumulative_types = 0
last_tokens = 0
last_types = 0
with open("rothman.unenriched.x-types.y-tokens.tsv", "w") as outf:
    for tokens_of_each, n_kmer_types in data:
        cumulative_tokens += n_kmer_types * tokens_of_each
        cumulative_types += n_kmer_types

        if (last_tokens == 0 or 
            (cumulative_tokens - last_tokens) / total_tokens > 0.01 or
            (cumulative_types - last_types) / total_types > 0.01 or
            cumulative_tokens/last_tokens > 1.1 or
            cumulative_types/last_types > 1.1):
            
            outf.write("%s\t%s\n" % (cumulative_types, cumulative_tokens))
            last_tokens = cumulative_tokens
            last_types = cumulative_types
            
    outf.write("%s\t%s\n" % (cumulative_types, cumulative_tokens))

cumulative_tokens = 0
last_tokens = 0
last_tokens_of_each = 0
with open("rothman.unenriched.x-tokens-sharing-type.y-tokens.tsv", "w") as outf:
    for tokens_of_each, n_kmer_types in data:
        cumulative_tokens += n_kmer_types * tokens_of_each

        if (last_tokens == 0 or 
            (cumulative_tokens - last_tokens) / total_tokens > 0.01 or
            cumulative_tokens/last_tokens > 1.1 or
            tokens_of_each/last_tokens_of_each > 1.1):

            outf.write("%s\t%s\n" % (tokens_of_each,
                                     cumulative_tokens/total_tokens))
            last_tokens = cumulative_tokens
            last_tokens_of_each = tokens_of_each
            
    outf.write("%s\t%s\n" % (tokens_of_each,
                             cumulative_tokens/total_tokens))
