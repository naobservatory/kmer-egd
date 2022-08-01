#include <stdlib.h>
#include <stdio.h>
#include <sys/mman.h>
#include <sys/errno.h>

int main(int argc, char** argv) {
  if (argc != 2) {
    printf("Usage: close-shm name\n");
    exit(1);
  }
  const char* shm_name = argv[1];
  int result = shm_unlink(shm_name);
  if (result < 0) {
    perror("Unable to close shared memory");
    exit(errno);
  }
}
