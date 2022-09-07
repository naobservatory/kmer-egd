#ifndef SHM_COMMON_H
#define SHM_COMMON_H

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define SHM_TYPE uint32_t
#define SHM_TYPE_MAX 0xffffffff

inline uint64_t shm_idx(uint64_t bucket, uint64_t day, uint64_t n_days) {
  return bucket * n_days + day;
}

uint64_t get_n_buckets_or_die(uint64_t n_bytes, uint64_t n_days) {
  if (n_bytes % (sizeof(SHM_TYPE) * n_days) != 0) {
    printf("error: n_bytes not divisible by %zu*n_days\n", sizeof(SHM_TYPE));
    exit(1);
  }
  return n_bytes / (sizeof(SHM_TYPE) * n_days);
}

#endif // SHM_COMMON_H
