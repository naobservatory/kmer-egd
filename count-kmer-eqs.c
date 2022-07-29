#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <fcntl.h>           /* For O_* constants */
#include <sys/stat.h>        /* For mode constants */
#include <sys/errno.h>
#include <unistd.h>
#include "util.h"
#include "shm-common.h"
#include "superfasthash.h"

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

void handle_kmers(char* circular_buffer, int offset, void* data_void) {
  struct data_t* data = (struct data_t*)data_void;

  uint64_t hash = HashGenomicCircularBuffer(circular_buffer, offset);

  // TODO(jefftk) Since we're modifying the shared memory in multiple threads
  // at once there's some possibilty of missing increments here.  They should
  // be pretty unlikely, however, since per-core cache is very small compared
  // to the size of the array (10s of MB vs 10s of GB).  A few dropped
  // increments is fine.  Since we're using aligned 32-bit integers on x86 I
  // don't think there are worse things that might happen.  Read more about the
  // best way to do this.
  uint64_t idx = hash % data->n_buckets;
  SHM_TYPE val = data->buckets[idx];
  if (val < SHM_TYPE_MAX) {
    data->buckets[idx] = val + 1;
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
