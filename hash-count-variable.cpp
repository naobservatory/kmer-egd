#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unordered_map>
#include "superfasthash.h"

#define K_4 10
#define K (K_4*4)
#define K_STR "40"

#define MAX_READ_LENGTH 151
#define DAYS 14

#define A 0
#define C 1
#define G 2
#define T 3

// TODO: use char[K/4] and pack them in with shifting
typedef std::array<char, K> KMer;
typedef std::array<unsigned char, K_4> PackedKMer;

unsigned char base_to_enum(char base) {
  switch (base) {
  case 'A': return A;
  case 'C': return C;
  case 'T': return T;
  default: return G;
  }
}

char enum_to_base(unsigned char base_enum) {
  switch (base_enum & 0b00000011) {
  case A: return 'A';
  case C: return 'C';
  case T: return 'T';
  default: return 'G';
  }
}

void pack_kmer(const KMer& in, PackedKMer& out) {
  for (int i = 0 ; i < K_4; i++) {
    out[i] =
      base_to_enum(in[i*4]) +
      (base_to_enum(in[i*4 + 1]) << 2) +
      (base_to_enum(in[i*4 + 2]) << 4) +
      (base_to_enum(in[i*4 + 3]) << 6);
  }
}

void unpack_kmer(const PackedKMer& in, KMer& out) {
  for (int i = 0 ; i < K_4; i++) {
    out[i*4] = enum_to_base(in[i]);
    out[i*4 + 1] = enum_to_base(in[i] >> 2);
    out[i*4 + 2] = enum_to_base(in[i] >> 4);
    out[i*4 + 3] = enum_to_base(in[i] >> 6);
  }
}

namespace std {
  template <> struct hash<PackedKMer> {
    std::size_t operator()(const PackedKMer& pk) const {
      return SuperFastHash((const char*)pk.data(), K_4);
    }
  };
}

typedef std::unordered_map<PackedKMer, std::array<uint32_t, DAYS>> Map;

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

    bool skip = false;

    KMer kmer;
    for (int j = 0; j < K; j++) {
      char c = read[i + j];
      if (c != 'A' && c != 'C' && c != 'G' && c != 'T') {
        skip = true;
        break;
      }
      kmer[j] = read[i + j];
    }

    if (skip) continue;

    PackedKMer packed_kmer;
    pack_kmer(kmer, packed_kmer);

    map[packed_kmer][day] += 1;
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
    KMer kmer;
    unpack_kmer(i.first, kmer);
    printf("%." K_STR "s", kmer);
    for (int day = 0; day < DAYS; day++) {
      printf("\t%u", i.second[day]);
    }
    printf("\n");
  }
}
