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

#define PRE_SHM_ARGS 4

int main(int argc, char** argv) {
  int n_days = argc-PRE_SHM_ARGS;
  if (n_days < 1) {
    printf("Usage: shm-dump-all n_buckets bucket_mods bucket_mod shm_names...\n");
    exit(1);
  }
  uint64_t n_buckets_per_shm = strtoll(argv[1], NULL, 10);
  uint64_t bucket_mods = strtoll(argv[2], NULL, 10);
  uint64_t bucket_mod = strtoll(argv[3], NULL, 10);
  SHM_TYPE* days[n_days];

  for (int day = 0; day < n_days; day++) {
    const char* shm_name = argv[day + PRE_SHM_ARGS];
    int result = shm_open(shm_name, O_RDONLY, S_IRUSR);
    if (result < 0) {
      printf("With %s:", shm_name);
      perror("Unable to open shared memory");
      exit(errno);
    }
    int fd = result;
    
    size_t len = n_buckets_per_shm * sizeof(SHM_TYPE);

    void* raw = mmap(0, len, PROT_READ, MAP_SHARED, fd, 0);
    if (raw == MAP_FAILED) {
      perror("Unable to mmap shared memory");
      exit(errno);
    }

    days[day] = (SHM_TYPE*)raw;
  }

  uint64_t sums[n_days];
  for (int day = 0; day < n_days; day++) {
    sums[day] = 0;
    for (int bucket = 0; bucket < n_buckets_per_shm; bucket++) {
      sums[day] += days[day][bucket];
    }
  }

  printf("sums");
  for (int day = 0; day < n_days; day++) {
    printf("\t%lu", sums[day]);
  }
  printf("\n");

  for (int bucket = 0; bucket < n_buckets_per_shm; bucket++) {
    if (bucket % bucket_mods != bucket_mod) continue;
    
    printf("%d", bucket);
    for (int day = 0; day < n_days; day++) {
      printf("\t%u", days[day][bucket]);
    }
    printf("\n");
  }
}
