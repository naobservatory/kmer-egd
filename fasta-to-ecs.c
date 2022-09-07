#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "superfasthash.h"
#include <sys/mman.h>
#include <fcntl.h>           /* For O_* constants */
#include <sys/stat.h>        /* For mode constants */
#include <sys/errno.h>
#include <unistd.h>
#include "util.h"

int main(int argc, char** argv) {
  if (argc != 2) {
    printf("Usage: fasta-to-kmers N_BUCKETS\n");
    exit(1);
  }
  uint64_t n_buckets = strtoll(argv[1], NULL, 10);

  char b;
  
  int seq_idx = 0;

  char kmer[K];
  char kmer_rc[K];
  
  while ((b = getchar_unlocked()) != EOF) {
    if (b == '>') {
      // skip  id line
      while ((b = getchar_unlocked()) != EOF && b != '\n');
      
      // what follows is a sequence
      seq_idx = 0;
    }
    // ignore linebreaks within sequence
    if (b == '\n') continue;

    for (int i = 1; i < K; i++) {
      kmer[i-1] = kmer[i];
      kmer_rc[K-i] = kmer_rc[K-i-1];
    }
    kmer_rc[0] = complement(b);
    kmer[K-1] = b;

    if (seq_idx >= K-1) {
      uint64_t hash = rc_agnostic_hash(kmer, kmer_rc);
      uint64_t bucket = hash % n_buckets;
      //printf("%." K_STR "s\t%lu\n", kmer, bucket);
      printf("%lu\n", bucket);
    }
    
    seq_idx++;
  }
}
