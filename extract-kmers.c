#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <fcntl.h>           /* For O_* constants */
#include <sys/stat.h>        /* For mode constants */
#include <sys/errno.h>
#include <unistd.h>
#include <stdbool.h>
#include "util.h"

struct data_t {
  uint64_t n_buckets;
  uint64_t* targets;
  int n_targets;
};

void handle_kmers(char* kmer, char* kmer_rc, void* data_void) {
  struct data_t* data = (struct data_t*)data_void;

  uint64_t hash = rc_agnostic_hash(kmer, kmer_rc);
  uint64_t idx = hash % data->n_buckets;
    
  for (int i = 0; i < data->n_targets; i++) {
    if (data->targets[i] == idx) {
      bool use_rc = strncmp(kmer, kmer_rc, K) > 0;
      printf("%." K_STR "s\t%lu\n", use_rc ? kmer_rc : kmer, idx);
    }
  }
}

int main(int argc, char** argv) {
  if (argc < 3) {
    printf("Usage: extract-kmers N_BUCKETS hash1 [hash2 [hash3 [...]]]\n");
    exit(1);
  }

  struct data_t data;
  data.n_buckets = strtoll(argv[1], NULL, 10);
  data.n_targets = argc - 2;
  data.targets = (uint64_t*)malloc(data.n_targets * sizeof(uint64_t));
  for (int i = 0; i < data.n_targets; i++) {
    data.targets[i] = strtoll(argv[i+2], NULL, 10);
  }
  
  iterate_kmers(handle_kmers, (void*)&data);  
}
