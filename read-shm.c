#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/mman.h>
#include <fcntl.h>           /* For O_* constants */
#include <sys/errno.h>
#include <unistd.h>
#include "shm-common.h"

int main(int argc, char** argv) {
  if (argc != 3) {
    printf("Usage: read-shm n_buckets bucket\n");
    exit(1);
  }
  uint64_t n_buckets = strtoll(argv[1], NULL, 10);
  uint64_t bucket = strtoll(argv[2], NULL, 10);

  int result = shm_open(SHM_NAME, O_RDONLY, S_IRUSR);
  if (result < 0) {
    perror("Unable to open shared memory");
    exit(errno);
  }
  int fd = result;

  size_t len = n_buckets * sizeof(SHM_TYPE);

  void* raw = mmap(0, len, PROT_READ, MAP_SHARED, fd, 0);
  if (raw == MAP_FAILED) {
    perror("Unable to mmap shared memory");
    exit(errno);
  }

  SHM_TYPE* region = (SHM_TYPE*)raw;
  printf("%s[%lu] = %u\n", SHM_NAME, bucket, region[bucket]);
}
