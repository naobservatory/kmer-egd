#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "superfasthash.h"

#define INITIAL 0
#define GOT_AT 1
#define IN_SEQ 2

#define K 40

char complement(char b) {
  switch (b) {
  case 'A': return 'T';
  case 'C': return 'G';
  case 'G': return 'C';
  case 'T': return 'A';
  default: return ' ';
  }
}

int main(int argc, char** argv) {
  if (argc != 2) {
    printf("Usage: count-kmer-eqs N_BUCKETS\n");
    exit(1);
  }
  uint64_t n_buckets = strtoll(argv[1], NULL, 10);

  char b;
  int state = INITIAL;
  int seq_idx = 0;

  char kmer[K];
  char kmer_rc[K];

  uint32_t* buckets = (uint32_t*)malloc(n_buckets * sizeof(uint32_t));

  while ((b = getchar_unlocked()) != EOF) {
    if (state == IN_SEQ && b != '\n' && b != '+') {
      if (seq_idx < K) {
        kmer[seq_idx] = b;
      } else {
        for (int i = 1; i < K; i++) {
          kmer[i-1] = kmer[i];
        }
        kmer[K-1] = b;
        for (int i = 0; i < K; i++) {
          kmer_rc[i] = complement(kmer[K-1-i]);
        }

        // We want:
        // * A 64 bit hash value, because n_buckets > 4B is possible.
        // * One that's identical between this K-mer or its reverse complement,
        //   since we could get either when reading DNA.
        // Compute the hashes of this K-mer and its reverse complement, sort,
        // and concatenate.
        uint32_t kmer_hash = SuperFastHash(kmer, K);
        uint32_t kmer_rc_hash = SuperFastHash(kmer_rc, K);
        uint64_t hash = kmer_hash < kmer_rc_hash ?
          (uint64_t)kmer_hash << 32 | kmer_rc_hash :
          (uint64_t)kmer_rc_hash << 32 | kmer_hash;
        uint32_t val = buckets[hash % n_buckets];
        if (val < 0xffffffff) {
          buckets[hash % n_buckets] = val + 1;
        }
      }
      seq_idx++;
    }

    if (state == INITIAL && b == '@') {
      state = GOT_AT;
    } else if (state == GOT_AT && b == '\n') {
      state = IN_SEQ;
      seq_idx = 0;
    } else if (state == IN_SEQ && b == '+') {
      state = INITIAL;
    }
  }

  for (size_t i = 0 ; i < n_buckets; i++) {
    printf("%d\n", buckets[i]);
  }
}
