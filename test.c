// usage: cat foo.fastq | ./test

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/errno.h>
#include <unistd.h>
#include "util.h"

struct data_t {
  uint64_t n_buckets;
  uint64_t* targets;
  int n_targets;
};

void handle_kmers(char* kmer, char* kmer_rc, void* ignored) {
  uint64_t hash1 = rc_agnostic_hash(kmer, kmer_rc);
  uint64_t hash2 = rc_agnostic_hash(kmer_rc, kmer);

  if (hash1 != hash2) {
    printf("Order-dependent hash when comparing %." K_STR "s and %." K_STR
           "s: %lu vs %lu\n", kmer, kmer_rc, hash1, hash2);
    exit(1);
  }

  for (int i = 0; i < K ; i++) {
    if (kmer[i] != complement(kmer_rc[K-1-i])) {
      printf("Mismatch when comparing %." K_STR "s and %." K_STR
             "s: %c vs %c at %d/%d\n", kmer, kmer_rc, kmer[i], kmer_rc[K-1-i],
             i, K-1-i);
      exit(1);
    }
  }
  //printf("%." K_STR "s %." K_STR "s\n", kmer, kmer_rc);
}

int main(int argc, char** argv) {
  iterate_kmers(handle_kmers, NULL);
}
