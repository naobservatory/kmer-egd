#ifndef UTIL_H
#define UTIL_H

#include <stdint.h>
#include <stdio.h>
#include "superfasthash.h"

#define K 40
#define K_STR "40"

#define INITIAL 0
#define GOT_AT 1
#define IN_SEQ 2

char complement(char b) {
  switch (b) {
  case 'A': return 'T';
  case 'C': return 'G';
  case 'G': return 'C';
  case 'T': return 'A';
  case 'N': return 'N';
  default: return ' ';
  }
}

// kmer and kmer_rc are both K long
uint32_t rc_agnostic_hash(char* kmer, char* kmer_rc) {
  // We want:
  // * A 64 bit hash value, because n_buckets > 4B is possible.
  // * One that's identical between this K-mer or its reverse complement,
  //   since we could get either when reading DNA.
  // Compute the hashes of this K-mer and its reverse complement, sort,
  // and concatenate.
  uint32_t kmer_hash = SuperFastHash(kmer, K);
  uint32_t kmer_rc_hash = SuperFastHash(kmer_rc, K);
  return kmer_hash < kmer_rc_hash ?
    (uint64_t)kmer_hash << 32 | kmer_rc_hash :
    (uint64_t)kmer_rc_hash << 32 | kmer_hash;
}

// kmer and kmer_rc are both K long
typedef void (*kmer_handler_t)(uint64_t read_index,
                               char* kmer,
                               char* kmer_rc,
                               void *data);

void iterate_kmers(kmer_handler_t kmer_handler, void* data) {
  char b;
  int state = INITIAL;
  int seq_index = 0;

  char kmer[K];
  char kmer_rc[K];

  uint64_t read_index = 0;

  while ((b = getchar_unlocked()) != EOF) {
    if (state == IN_SEQ && b != '\n' && b != '+') {
      for (int i = 1; i < K; i++) {
        kmer[i-1] = kmer[i];
        kmer_rc[K-i] = kmer_rc[K-i-1];
      }
      kmer_rc[0] = complement(b);
      kmer[K-1] = b;

      if (seq_index >= K-1) {
        kmer_handler(read_index, kmer, kmer_rc, data);
      }
      seq_index++;
    }

    if (state == INITIAL && b == '@') {
      state = GOT_AT;
    } else if (state == GOT_AT && b == '\n') {
      state = IN_SEQ;
      seq_index = 0;
    } else if (state == IN_SEQ && b == '+') {
      state = INITIAL;
      /*
      if (read_index % 10000 == 0) {
        printf("Finished read %lu\n", read_index);
      }
      */
      read_index++;
    }
  }
}


#endif // UTIL_H
