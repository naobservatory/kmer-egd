#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/mman.h>
#include <fcntl.h>           /* For O_* constants */
#include <sys/stat.h>        /* For mode constants */
#include <sys/errno.h>
#include <unistd.h>
#include "shm-common.h"

int main(int argc, char** argv) {
  if (argc != 2) {
    printf("Usage: open-shm N_BUCKETS\n");
    exit(1);
  }
  uint64_t n_buckets = strtoll(argv[1], NULL, 10);

  int result = shm_open(SHM_NAME, O_RDWR | O_CREAT | O_EXCL,
                        S_IRUSR | S_IWUSR);
  if (result < 0) {
    perror("Unable to open shared memory");
    exit(errno);
  }
  int fd = result;

  size_t len = n_buckets * sizeof(SHM_TYPE);
  result = ftruncate(fd, len);
  if (result < 0) {
    perror("Unable to size shared memory");
    exit(errno);
  }

  void* raw = mmap(0, len, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
  if (raw == MAP_FAILED) {
    perror("Unable to mmap shared memory");
    exit(errno);
  }
}
