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
  int n_days = argc-2;
  if (n_days < 1) {
    printf("Usage: shm-egd n_buckets shm_names...\n");
    exit(1);
  }
  uint64_t n_buckets_per_shm = strtoll(argv[1], NULL, 10);
  SHM_TYPE* days[n_days];

  for (int day = 0; day < n_days; day++) {
    const char* shm_name = argv[day + 2];
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
  
  double logs[n_days];
  double log_deltas[n_days - 1];

  int printed = 0;
  for (int bucket = 0; bucket < n_buckets_per_shm; bucket++) {
    if (days[n_days - 1][bucket] < 8) continue;
    
    double avg_delta = 0;
    for (int day = 0; day < n_days; day++) {
      logs[day] = log(1.0 * days[day][bucket] / sums[day]);
      if (day > 0) {
        log_deltas[day] = logs[day] - logs[day - 1];
      }
      avg_delta += log_deltas[day];
    }
    avg_delta /= (n_days - 1);

    if (avg_delta < 0.05) continue;
    
    double sum_err_sq = 0;
    for (int day = 0; day < n_days - 1; day++) {
      double err = log_deltas[day] - avg_delta;
      sum_err_sq += (err * err);
    }
    double rms_error = sqrt(sum_err_sq / n_days- 1);
    if (rms_error != rms_error) continue; // skip NaN

    printf("%0.4lf %0.4lf", rms_error, avg_delta);
    
    // if (days[n_days - 1][bucket] < 16) continue;

    /*
    bool is_biggest = true;
    for (int day = 0; day < n_days - 1; day++) {
      if (days[day][bucket] >= days[n_days - 1][bucket]) {
        is_biggest = false;
        break;
      }
    }
    if (!is_biggest) continue;
    */

    /*
    bool is_monotonic = true;
    for (int day = 0; day < n_days - 1; day++) {
      if (days[day][bucket] > days[day + 1][bucket]) {
        is_monotonic = false;
        break;
      }
    }
    if (!is_monotonic) continue;
    */

    /*
    bool is_growingish = true;
    for (int day = 0; day < n_days - 1; day++) {
      if (days[day][bucket] < 4) continue;
      if (days[day][bucket] * 0.8 > days[day + 1][bucket]) {
        is_growingish = false;
        break;
      }
    }
    if (!is_growingish) continue;
    */

    

    printf(" %09d", bucket);
    for (int day = 0; day < n_days; day++) {
      printf(" %u/%lu", days[day][bucket], sums[day]);
    }
    printf("\n");
    printed++;
    //if (printed > 20) break;
  }
}
