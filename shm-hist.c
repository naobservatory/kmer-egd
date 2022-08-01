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
    printf("Usage: read-shm shm_name n_buckets\n");
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

  uint64_t histogram[32];
  uint64_t sizes[32];
  uint64_t thresholds[32];
  uint64_t threshold = 1;
  for (int i = 0 ; i < 32; i++) {
    histogram[i] = 0;
    sizes[i] = 0;
    thresholds[i] = threshold;
    threshold *= 2;
  }

  SHM_TYPE* region = (SHM_TYPE*)raw;


  // What do our equivalence classes look like?
  for (uint64_t i = 0; i < n_buckets; i++) {
    // This is about 6x faster than looping over histogram/sizes/thresholds
    // sadly.
    if (region[i] > 0x0) { histogram[0]++; sizes[0] += region[i]; }
    if (region[i] > 0x1) { histogram[1]++; sizes[1] += region[i]; }
    if (region[i] > 0x2) { histogram[2]++; sizes[2] += region[i]; }
    if (region[i] > 0x4) { histogram[3]++; sizes[3] += region[i]; }
    if (region[i] > 0x8) { histogram[4]++; sizes[4] += region[i]; }
    if (region[i] > 0x10) { histogram[5]++; sizes[5] += region[i]; }
    if (region[i] > 0x20) { histogram[6]++; sizes[6] += region[i]; }
    if (region[i] > 0x40) { histogram[7]++; sizes[7] += region[i]; }
    if (region[i] > 0x80) { histogram[8]++; sizes[8] += region[i]; }
    if (region[i] > 0x100) { histogram[9]++; sizes[9] += region[i]; }
    if (region[i] > 0x200) { histogram[10]++; sizes[10] += region[i]; }
    if (region[i] > 0x400) { histogram[11]++; sizes[11] += region[i]; }
    if (region[i] > 0x800) { histogram[12]++; sizes[12] += region[i]; }
    if (region[i] > 0x1000) { histogram[13]++; sizes[13] += region[i]; }
    if (region[i] > 0x2000) { histogram[14]++; sizes[14] += region[i]; }
    if (region[i] > 0x4000) { histogram[15]++; sizes[15] += region[i]; }
    if (region[i] > 0x8000) { histogram[16]++; sizes[16] += region[i]; }
    if (region[i] > 0x10000) { histogram[17]++; sizes[17] += region[i]; }
    if (region[i] > 0x20000) { histogram[18]++; sizes[18] += region[i]; }
    if (region[i] > 0x40000) { histogram[19]++; sizes[19] += region[i]; }
    if (region[i] > 0x80000) { histogram[20]++; sizes[20] += region[i]; }
    if (region[i] > 0x100000) { histogram[21]++; sizes[21] += region[i]; }
    if (region[i] > 0x200000) { histogram[22]++; sizes[22] += region[i]; }
    if (region[i] > 0x400000) { histogram[23]++; sizes[23] += region[i]; }
    if (region[i] > 0x800000) { histogram[24]++; sizes[24] += region[i]; }
    if (region[i] > 0x1000000) { histogram[25]++; sizes[25] += region[i]; }
    if (region[i] > 0x2000000) { histogram[26]++; sizes[26] += region[i]; }
    if (region[i] > 0x4000000) { histogram[27]++; sizes[27] += region[i]; }
    if (region[i] > 0x8000000) { histogram[28]++; sizes[28] += region[i]; }
    if (region[i] > 0x10000000) { histogram[29]++; sizes[29] += region[i]; }
    if (region[i] > 0x20000000) { histogram[30]++; sizes[30] += region[i]; }
    if (region[i] > 0x40000000) { histogram[31]++; sizes[31] += region[i]; }
  }

  for (int i = 0 ; i < 32; i++) {
    printf(">%lu\t%lu\t%lu\n",
           thresholds[i]/2,
           histogram[i],
           sizes[i]);
  }
}
