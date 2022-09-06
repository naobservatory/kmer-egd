#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/mman.h>
#include <fcntl.h>           /* For O_* constants */
#include <sys/errno.h>
#include <unistd.h>
#include <math.h>
#include "shm-common.h"

int main(int argc, char** argv) {
  if (argc != 4) {
    printf("Usage: shm-dump-all n_bytes shm_name n_days\n");
    exit(1);
  }
  uint64_t n_bytes = strtoll(argv[1], NULL, 10);
  uint64_t n_days = strtoll(argv[3], NULL, 10);
  uint64_t n_buckets = get_n_buckets_or_die(n_bytes, n_days);

  SHM_TYPE* shm;
  
  const char* shm_name = argv[2];
  int result = shm_open(shm_name, O_RDONLY, S_IRUSR);
  //int result = shm_open(shm_name, O_RDWR, S_IRUSR);
  if (result < 0) {
    printf("With %s:", shm_name);
    perror("Unable to open shared memory");
    exit(errno);
  }
  int fd = result;
  
  void* raw = mmap(0, n_bytes, PROT_READ, MAP_SHARED, fd, 0);
  //void* raw = mmap(0, n_bytes, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
  if (raw == MAP_FAILED) {
    perror("Unable to mmap shared memory");
    exit(errno);
  }

  shm = (SHM_TYPE*)raw;

  /*
  printf("setting!\n");
  for (uint64_t bucket = 0; bucket < n_buckets; bucket++) {
    for (uint64_t day = 0; day < n_days; day++) {
      shm[shm_idx(bucket, day, n_days)] = 1;
    }
  }
  printf("set!\n");
  return 0; 
  */

  /*
  uint64_t sums[n_days];
  for (uint64_t day = 0; day < n_days; day++) sums[day] = 0;
        
  for (uint64_t bucket = 0; bucket < n_buckets; bucket++) {
    for (uint64_t day = 0; day < n_days; day++) {
      sums[day] += shm[shm_idx(bucket, day, n_days)];
    }
  }

  printf("sums");
  for (uint64_t day = 0; day < n_days; day++) {
    printf("\t%lu", sums[day]);
  }
  printf("\n");
  */
  
  for (uint64_t bucket = 0; bucket < n_buckets; bucket++) {
    printf("%lu", bucket);
    for (uint64_t day = 0; day < n_days; day++) {
      printf("\t%u", shm[shm_idx(bucket, day, n_days)]);
    }
    printf("\n");
  }
}
