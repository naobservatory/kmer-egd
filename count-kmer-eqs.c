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
#include "shm-common.h"

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

struct data_t {
  uint64_t n_buckets;
  SHM_TYPE* buckets;
};

void handle_kmers(char* kmer, char* kmer_rc, void* data_void) {
  struct data_t* data = (struct data_t*)data_void;

  uint64_t hash = rc_agnostic_hash(kmer, kmer_rc);

  uint64_t idx = hash % data->n_buckets;
  SHM_TYPE* bucket_ptr = &(data->buckets[idx]);
  SHM_TYPE val = __atomic_load_n(bucket_ptr, __ATOMIC_RELAXED);
  if (val < SHM_TYPE_MAX) {
    // A dropped write is possible here if another CPU is trying to increment
    // this bucket at the same time.  Very unlikely, though, since we have so
    // many buckets.  And we're somewhat robust to dropped writes.
    __atomic_store_n(bucket_ptr, val + 1, __ATOMIC_RELAXED);
  }
}

int main(int argc, char** argv) {
  if (argc != 2) {
    printf("Usage: count-kmer-eqs N_BUCKETS\n");
    exit(1);
  }

  struct data_t data;
  data.n_buckets = strtoll(argv[1], NULL, 10);
  data.buckets = open_shm(data.n_buckets);

  iterate_kmers(handle_kmers, (void*)&data);  
}
