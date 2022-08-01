#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/mman.h>
#include <fcntl.h>           /* For O_* constants */
#include <sys/errno.h>
#include <unistd.h>
#include "shm-common.h"

int main(int argc, char** argv) {
  if (argc != 2) {
    printf("Usage: shm-examples shm_name n_buckets\n");
    exit(1);
  }
  const char* shm_name = argv[1];
  uint64_t n_buckets = strtoll(argv[2], NULL, 10);

  int result = shm_open(shm_name, O_RDONLY, S_IRUSR);
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

  uint64_t examples[32];
  uint64_t thresholds[32];
  uint64_t threshold = 1;
  for (int i = 0 ; i < 32; i++) {
    examples[i] = 0;
    thresholds[i] = threshold;
    threshold *= 2;
  }

  SHM_TYPE* region = (SHM_TYPE*)raw;

  for (uint64_t i = 0; i < n_buckets; i++) {
    if (region[i] > 0x0) { examples[0] = i; }
    if (region[i] > 0x1) { examples[1] = i; }
    if (region[i] > 0x2) { examples[2] = i; }
    if (region[i] > 0x4) { examples[3] = i; }
    if (region[i] > 0x8) { examples[4] = i; }
    if (region[i] > 0x10) { examples[5] = i; }
    if (region[i] > 0x20) { examples[6] = i; }
    if (region[i] > 0x40) { examples[7] = i; }
    if (region[i] > 0x80) { examples[8] = i; }
    if (region[i] > 0x100) { examples[9] = i; }
    if (region[i] > 0x200) { examples[10] = i; }
    if (region[i] > 0x400) { examples[11] = i; }
    if (region[i] > 0x800) { examples[12] = i; }
    if (region[i] > 0x1000) { examples[13] = i; }
    if (region[i] > 0x2000) { examples[14] = i; }
    if (region[i] > 0x4000) { examples[15] = i; }
    if (region[i] > 0x8000) { examples[16] = i; }
    if (region[i] > 0x10000) { examples[17] = i; }
    if (region[i] > 0x20000) { examples[18] = i; }
    if (region[i] > 0x40000) { examples[19] = i; }
    if (region[i] > 0x80000) { examples[20] = i; }
    if (region[i] > 0x100000) { examples[21] = i; }
    if (region[i] > 0x200000) { examples[22] = i; }
    if (region[i] > 0x400000) { examples[23] = i; }
    if (region[i] > 0x800000) { examples[24] = i; }
    if (region[i] > 0x1000000) { examples[25] = i; }
    if (region[i] > 0x2000000) { examples[26] = i; }
    if (region[i] > 0x4000000) { examples[27] = i; }
    if (region[i] > 0x8000000) { examples[28] = i; }
    if (region[i] > 0x10000000) { examples[29] = i; }
    if (region[i] > 0x20000000) { examples[30] = i; }
    if (region[i] > 0x40000000) { examples[31] = i; }
  }

  for (int i = 0 ; i < 32; i++) {
    printf(">%lu\t%lu\n",
           thresholds[i]/2,
           examples[i]);
  }
}
