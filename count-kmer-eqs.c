#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "superfasthash.h"
#include <sys/mman.h>
#include <fcntl.h>           /* For O_* constants */
#include <sys/stat.h>        /* For mode constants */
#include <sys/errno.h>
#include <unistd.h>
#include "shm-common.h"

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

SHM_TYPE* open_shm(uint64_t n_buckets) {
  int result = shm_open(SHM_NAME, O_RDWR, S_IRUSR | S_IWUSR);
  if (result < 0) {
    perror("Unable to open shared memory");
    exit(errno);
  }
  int fd = result;
  size_t len = n_buckets * sizeof(SHM_TYPE);
  void* raw = mmap(0, len, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
  if (raw == MAP_FAILED) {
    perror("Unable to mmap shared memory");
    exit(errno);
  }
  return (SHM_TYPE*)raw;
}

int main(int argc, char** argv) {
  if (argc != 2) {
    printf("Usage: count-kmer-eqs N_BUCKETS\n");
    exit(1);
  }
  uint64_t n_buckets = strtoll(argv[1], NULL, 10);
  SHM_TYPE* buckets = open_shm(n_buckets);
  
  char b;
  int state = INITIAL;
  int seq_idx = 0;

  char kmer[K];
  char kmer_rc[K];

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

        // TODO(jefftk) Since we're modifying the shared memory in multiple
        // threads at once there's some possibilty of missing increments here.
        // They should be pretty unlikely, however, since per-core cache is
        // very small compared to the size of the array (10s of MB vs 10s of
        // GB).  A few dropped increments is fine.  Since we're using aligned
        // 32-bit integers on x86 I don't think there are worse things that
        // might happen.  Read more about the best way to do this.
        SHM_TYPE val = buckets[hash % n_buckets];
        if (val < SHM_TYPE_MAX) {
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
