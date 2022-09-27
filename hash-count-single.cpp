#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unordered_map>
#include <unordered_set>
#include <cstdint>

#include "superfasthash.h"

#define K_4 10
#define K (K_4*4)
#define K_STR "40"

#define MAX_READ_LENGTH 151

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

void* zmalloc(size_t size) {
  void* m = malloc(size);
  memset(m, 0, size);
  return m;
}

typedef std::unordered_map<PackedKMer, uint32_t> Map;

// https://support.illumina.com/bulletins/2016/12/what-sequences-do-i-use-for-adapter-trimming.html
#define ADAPTER "CTGTCTCTTATACACATCT"
#define ADAPTER_LEN 19

int trim_poly_g(char* read, int read_len) {
  int poly_g_count = 0;
  for (int i = read_len - 1; i >> 0 && read[i] == 'G'; i--) {
    poly_g_count++;
  }
  if (poly_g_count > 7) {
    read_len -= poly_g_count;
  }
  return read_len;
}
int trim_adapters(char* read, int read_len) {
  for (int i = 0; i < read_len - ADAPTER_LEN; i++) {
    int j;
    for (j = 0; j < ADAPTER_LEN && read[i + j] == ADAPTER[j]; j++);
    if (j == ADAPTER_LEN) {
      // This means the for loop got all the way through ADAPTER matching
      // constantly, so trim the read down to just before the adapter match.
      return i;
    }
  }
  return read_len;
}

void handle_read(char* read, int read_len, Map& map,
                 char* kmer_include, char* kmer_exclude) {
  /*
  printf("\n");
  for (int i = 0; i < read_len; i++) {
    printf("%c", read[i]);
  }
  printf("\n");
  */
  read_len = trim_adapters(read, read_len);
  read_len = trim_poly_g(read, read_len);
  /*
  for (int i = 0; i < read_len; i++) {
    printf("%c", read[i]);
  }
  printf("\n");
  */

  if (read_len < K) return;

  std::unordered_set<PackedKMer> seen;
  
  // Iterate over kmers in this read.
  for (int i = 0; i < read_len - K; i++) {
    // Ignore any kmers that aren't in the region we're trying to test.
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

    // Don't count the same K-mer multiple times in a single read.
    if (seen.find(packed_kmer) != seen.end()) continue;

    map[packed_kmer]++;
    seen.insert(packed_kmer);
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

  Map map;

  // $ time aws s3 ls s3://prjna729801/  | grep AA..-40-14.tsv.gz | awk '{print
  // $NF}' | xargs -P 32 -I {} bash -c "aws s3 cp s3://prjna729801/{} - |
  // gunzip | wc -l > {}.tmp.allcount"
  // $ cat *.allcount | awk '{sum+=$1}END{print sum}'
  //  953683196
  // But this is missing Kmers with lots of Gs, almost off by a factor of 2
  // Let's try reserving 2B
  map.reserve(2000000000L);
  
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
      handle_read(read, seq_idx, map, kmer_include, kmer_exclude);
      seq_idx = 0;
    }
    prev = b;
  }

  for (auto i : map) {
    printf("%u\n", i.second);
  }
}
