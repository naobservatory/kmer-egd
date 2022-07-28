#include <stdlib.h>
#include <stdio.h>
#include <sys/mman.h>
#include <sys/errno.h>
#include "shm-common.h"

int main(int argc, char** argv) {
  if (argc != 1) {
    printf("Usage: close-shm\n");
    exit(1);
  }
  int result = shm_unlink(SHM_NAME);
  if (result < 0) {
    perror("Unable to close shared memory");
    exit(errno);
  }
}
