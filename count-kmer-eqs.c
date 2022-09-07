#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <fcntl.h>           /* For O_* constants */
#include <sys/stat.h>        /* For mode constants */
#include <sys/errno.h>
#include <unistd.h>
#include "superfasthash.h"
#include "util.h"
#include "shm-common.h"

// Layout:
//   
SHM_TYPE* open_shm(const char* shm_name, uint64_t n_bytes) {
  int result = shm_open(shm_name, O_RDWR, S_IRUSR | S_IWUSR);
  if (result < 0) {
    perror("Unable to open shared memory");
    exit(errno);
  }
  int fd = result;
  void* raw = mmap(0, n_bytes, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
  if (raw == MAP_FAILED) {
    perror("Unable to mmap shared memory");
    exit(errno);
  }
  return (SHM_TYPE*)raw;
}

struct data_t {
  uint64_t n_bytes;
  uint64_t n_days;
  uint64_t n_buckets;
  uint64_t n_mods;
  uint64_t mod;
  SHM_TYPE* shm;
};

void handle_kmers(uint64_t read_index,
                  char* kmer,
                  char* kmer_rc,
                  void* data_void) {
  struct data_t* data = (struct data_t*)data_void;

  uint64_t hash = rc_agnostic_hash(kmer, kmer_rc);

  if (hash % data->n_mods != data->mod) return;

  uint64_t n_days = data->n_days;
  uint64_t day = read_index % n_days;
  uint64_t bucket = hash % data->n_buckets;
  SHM_TYPE* bucket_ptr = &(data->shm[shm_idx(bucket, day, n_days)]);         
  SHM_TYPE val = __atomic_load_n(bucket_ptr, __ATOMIC_RELAXED);
  if (val < SHM_TYPE_MAX) {
    // A dropped write is possible here if another CPU is trying to increment
    // this bucket at the same time.  Very unlikely, though, since we have so
    // many buckets.  And we're somewhat robust to dropped writes.
    __atomic_store_n(bucket_ptr, val + 1, __ATOMIC_RELAXED);
  }
}

int main(int argc, char** argv) {
  if (argc != 6) {
    // n_bytes: size of shared memory segment.  Must be a multiple of n_days.
    // shm_name: shared memory n_bytes size.  Should already be created.  Use
    //   open-shm.
    // n_days: how many days to simulate.  Uses read index % n_days to choose
    //   day.
    // n_mods: how many chunks to divide the hash space into
    // mod: which chunk we should be working with
    printf("Usage: count-kmer-eqs n_bytes shm_name n_days n_mods mod\n");
    exit(1);
  }
  struct data_t data;
  data.n_bytes = strtoll(argv[1], NULL, 10);
  data.n_days = strtoll(argv[3], NULL, 10);
  data.n_buckets = get_n_buckets_or_die(data.n_bytes, data.n_days);
  data.n_mods = strtoll(argv[4], NULL, 10);
  data.mod = strtoll(argv[5], NULL, 10);

  data.shm = open_shm(argv[2], data.n_bytes);
  
  //printf("Processing %lu/%lu with %lu buckets\n", data.mod, data.n_mods,
  //       data.n_buckets); 
  iterate_kmers(handle_kmers, (void*)&data);
  //printf("Complete.\n");
}
