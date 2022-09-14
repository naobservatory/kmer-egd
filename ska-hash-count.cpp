#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unordered_map>
#include "superfasthash.h"
#include "flat_hash_map.hpp"

#define K 40
#define K_STR "40"

#define MAX_READ_LENGTH 151
#define DAYS 14

// TODO: use char[K/4] and pack them in with shifting
typedef std::array<char, K> KMer;

namespace std {
  template <> struct hash<KMer> {
    std::size_t operator()(const KMer& k) const {
      return SuperFastHash(k.data(), K);
    }
  };
}

typedef ska::flat_hash_map<KMer, std::array<uint32_t, DAYS>> Map;

void handle_read(char* read, int read_len, int day, Map& map,
                 char* kmer_include, char* kmer_exclude) {
  int poly_g_count = 0;
  for (int i = read_len; i > 0; i--) {
    if (read[i] == 'G') {
      poly_g_count++;
    }
  }
  if (poly_g_count > 7) {
    read_len -= poly_g_count;
  }
  if (read_len == 0) {
    return;
  }

  // Iterate over kmers in this read.
  for (int i = 0; i < read_len - K + 1; i++) {
    if (strncmp(read + i, kmer_include, K) < 0) continue;
    if (strncmp(read + i, kmer_exclude, K) >= 0) continue;

    KMer kmer;
    for (int j = 0; j < K; j++) {
      kmer[j] = read[i + j];
    }

    map[kmer][day] += 1;
  }
}

int main(int argc, char** argv) {
  if (argc != 3) {
    fprintf(stderr, "usage: %s kmer_include kmer_exclude\n", argv[0]);
    return 1;
  }
  char* kmer_include = argv[1];
  char* kmer_exclude = argv[2];

  if (strlen(kmer_include) != K) {
    fprintf(stderr, "kmer_include length != %d\n", K);
    return 1;
  }
  if (strlen(kmer_exclude) != K) {
    fprintf(stderr, "kmer_exclude length != %d\n", K);
    return 1;
  }

  char b;
  char prev = '\n';

  int seq_idx = 0;
  char read[MAX_READ_LENGTH];

  int read_num = 0;

  Map map;
  
  // This reads a FASTQ file under a few assumptions that happen to be true
  // with our data:
  //  - sequence is all one line, with no \n
  //  - no quality line starts with @
  while ((b = getchar_unlocked()) != EOF) {
    if (prev == '\n' && b == '@') {
      // Skip the id line.
      while ((b = getchar_unlocked()) != EOF && b != '\n');
      // Read the sequence line.
      while ((b = getchar_unlocked()) != EOF && b != '\n') {
        if (seq_idx >= MAX_READ_LENGTH) {
          fprintf(stderr, "Read too long\n");
          exit(1);
        }

        read[seq_idx++] = b;
      }
      handle_read(read, seq_idx, read_num % DAYS, map, kmer_include,
                  kmer_exclude);
      seq_idx = 0;
      read_num++;
    }
    prev = b;
  }

  for (auto i : map) {
    printf("%." K_STR "s", i.first);
    for (int day = 0; day < DAYS; day++) {
      printf("\t%u", i.second[day]);
    }
    printf("\n");
  }
}
