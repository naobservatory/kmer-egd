/* Counts the k-mers in the unenriched portion of the Rothman 2021 data.
 *
 * Usage:
 *
 *   cat *.fastq.gz | \
 *      hash-count-rothman HTP AA AT | \
 *      gzip > counts_HTP_AA-AT.gz
 *
 *
 * It reads the metadata from rothman.unenriched.simple and interprets the ID
 * lines in the input fastq to figure out which day this
 * input corresponds to.
 *
 * The reason for k-mer prefixes is that otherwise we'd need too much memory to
 * store all the exact counts.
 *
 * Counts are initially stored as three bits per day packed into an int.  If
 * we see something more often than this can represent we switch to an array of
 * counts.  This array saturates, so if we see something a very large number of
 * times we can't tell exactly how many.
 */

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

#define MAX_READ_LENGTH 300
#define MAX_DAYS 21
#define ID_LEN 11  // ex: SRR14530899
#define DATE_LEN 10  // ex: 2020-09-23
#define WTP_OFFSET (ID_LEN + DATE_LEN + 2 ) // two tabs

int days;
char metadata[ID_LEN*MAX_DAYS];

#define A 0
#define C 1
#define G 2
#define T 3

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

#define COMPRESSED_COUNTS 1

void* zmalloc(size_t size) {
  void* m = malloc(size);
  memset(m, 0, size);
  return m;
}

// compressed_counts size is 64
// one bit for COMPRESSED_COUNTS flag, leaves 63 bits
// max days is 21 (HTP)
// 63 / 21 = 3 exactly -- lucky!
// this lets us store up to seven observations (0b111) before we need to switch
// to an array.
#define extract_compressed_count(compressed_counts, index) ((compressed_counts >> (index*3+1)) & 0b111)

class DayCounts {
private:
  union {
    // Pretty sure punning a pointer with an int is undefined behavior, but
    // good enough for prototyping.
    uint16_t* day_counts;
    uint64_t compressed_counts;
  };

public:
  DayCounts() {
    compressed_counts = COMPRESSED_COUNTS;
  }

  void increment(int day) {
    //printf("day: %d\n", day);
    //printf("before: ");
    //print();

    if (compressed_counts & COMPRESSED_COUNTS) {
      if (extract_compressed_count(compressed_counts, day) != 0b111) {
        compressed_counts += (1L << (day*3 + 1));
      } else {
        uint64_t saved_compressed_counts = compressed_counts;
        day_counts = (uint16_t*)zmalloc(sizeof(uint16_t)*days);
        for (int i = 0 ; i < days; i++) {
          day_counts[i] = extract_compressed_count(saved_compressed_counts, i);
        }
        day_counts[day]++;
      }
    } else {
      if (day_counts[day] < UINT16_MAX) {
        day_counts[day]++;
      }
    }

    //printf("after:  ");
    //print();
  }

  uint16_t get(int day) {
    if (compressed_counts & COMPRESSED_COUNTS) {
      return extract_compressed_count(compressed_counts, day);
    } else {
      return day_counts[day];
    }
  }

  void print() {
    for (int i = 0; i < days; i++) {
      printf("%u, ", get(i));
    }
    printf("\n");
  }

  void clear() {
    if (!(compressed_counts & COMPRESSED_COUNTS)) {
      free(day_counts);
    }
    compressed_counts = COMPRESSED_COUNTS;
  }
};

// sets the globals metadata days
void load_metadata(char* wtp) {
  FILE* inf = fopen("rothman.unenriched.simple", "r");
  if (inf == NULL) {
    perror("Can't open metadata");
    exit(1);
  }

  days = 0;

  char* line = NULL;
  size_t len = 0;
  ssize_t read;

  while ((read = getline(&line, &len, inf)) != -1) {
    // days are always in increasing order
    //printf("%s", line);
    //printf("%s %s\n", wtp, line + WTP_OFFSET);

    if (strncmp(wtp, line + WTP_OFFSET, strlen(wtp)) == 0) {
      for (int i = 0; i < ID_LEN; i++) {
        metadata[days*ID_LEN + i] = line[i];
      }
      days++;
    }
  }

  free(line);
  fclose(inf);

  if (days > MAX_DAYS) {
    fprintf(stderr, "too many days: %d > %d\n", days, MAX_DAYS);
    exit(1);
  }

  //for (int i = 0; i < days; i++) {
  //  printf("%d: %.11s\n", i, metadata + (i*ID_LEN));
  //}
}



typedef std::unordered_map<PackedKMer, DayCounts> Map;

void handle_read(char* read, int read_len, int day, Map& map,
                 char* kmer_include, char* kmer_exclude) {
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

    map[packed_kmer].increment(day);
    seen.insert(packed_kmer);
  }
}

void test() {
  days = MAX_DAYS;
  DayCounts dc;

  // Test that it's initially zero.
  for (int i = 0 ; i < days; i++) {
    if (dc.get(i) != 0) {
      fprintf(stderr, "non-zero initial dc at %d\n", i);
      exit(1);
    }
  }

  // Test that incrementing any individual spot leaves everything else at zero.
  for (int j = 0 ; j < days; j++) {
    dc.clear();
    dc.increment(j);
    for (int i = 0 ; i < days; i++) {
      if (i == j) {
        if (dc.get(j) != 1) {
          fprintf(stderr, "bad dc[%d] after increment[%d] = %u\n", j, i, dc.get(i));
          exit(1);
        }
      } else {
        if (dc.get(i) != 0) {
          fprintf(stderr, "non-zero dc[%d] after increment = %u\n", i, dc.get(i));
          exit(1);
        }
      }
    }
  }

  // Test that incrementing any individual spot twice leaves everything else at
  // zero.
  for (int j = 0 ; j < days; j++) {
    dc.clear();
    dc.increment(j);
    dc.increment(j);
    for (int i = 0 ; i < days; i++) {
      if (i == j) {
        if (dc.get(j) != 2) {
          fprintf(stderr, "bad dc[%d] after increment[%d] = %u\n", j, i, dc.get(i));
          exit(1);
        }
      } else {
        if (dc.get(i) != 0) {
          fprintf(stderr, "non-zero dc[%d] after increment = %u\n", i, dc.get(i));
          exit(1);
        }
      }
    }
  }

  // Test that incrementing any individual spot twice leaves everything else at
  // one.
  for (int j = 0 ; j < days; j++) {
    dc.clear();
    for (int i = 0 ; i < days; i++) {
      dc.increment(i);
    }
    dc.increment(j);
    for (int i = 0 ; i < days; i++) {
      if (i == j) {
        if (dc.get(j) != 2) {
          fprintf(stderr, "bad dc[%d] after increment[%d] = %u\n", j, i, dc.get(i));
          exit(1);
        }
      } else {
        if (dc.get(i) != 1) {
          fprintf(stderr, "non-one dc[%d] after increment = %u\n", i, dc.get(i));
          exit(1);
        }
      }
    }
  }

  // Test that we can store many different values;
  dc.clear();
  for (int j = 0 ; j < days; j++) {
    for (int i = j + 1; i < days; i++) {
      dc.increment(i);
    }
  }
  // validate
  for (int i = 0 ; i < days; i++) {
    if (dc.get(i) != i) {
      fprintf(stderr, "bad dc[%d] after incrementing %d times = %u\n", i, i, dc.get(i));
      exit(1);
    }
  }

  // Test saturation
  dc.clear();
  for (int i = 0; i < UINT16_MAX + 5; i++) {
    int expected = i < UINT16_MAX ? i : UINT16_MAX;
    if (dc.get(7) != expected) {
      fprintf(stderr,
              "bad dc[7] after incrementing %d times: got %d expected %d\n",
              i, dc.get(7), expected);
    }
    dc.increment(7);
  }
}

int main(int argc, char** argv) {
  test();  // So fast that we might as well do it every time.

  if (argc != 3) {
    fprintf(stderr, "usage: %s wtp prefix\n", argv[0]);
    return 1;
  }

  char* wtp = argv[1];
  char* prefix= argv[2];

  char kmer_include[K+1] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA";
  char kmer_exclude[K+1] = "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ";

  for(int i = strlen(prefix) - 1 ; i >= 0;  i--) {
    kmer_include[i] = prefix[i];
  }
  for(int i = strlen(prefix) - 1 ; i >= 0;  i--) {
    kmer_exclude[i] = prefix[i];
  }

  if (strlen(kmer_include) != K) {
    fprintf(stderr, "kmer_include length != %d\n", K);
    return 1;
  }
  if (strlen(kmer_exclude) != K) {
    fprintf(stderr, "kmer_exclude length != %d\n", K);
    return 1;
  }

  load_metadata(wtp);

  char b;
  char prev = '\n';

  int seq_idx = 0;
  char read[MAX_READ_LENGTH];

  char id[ID_LEN];

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
      for (int i = 0; i < ID_LEN; i++) {
        id[i] = getchar_unlocked();
      }
      // Skip the rest of the id line.
      while ((b = getchar_unlocked()) != EOF && b != '\n');
      // Read the sequence line.
      while ((b = getchar_unlocked()) != EOF && b != '\n') {
        if (seq_idx >= MAX_READ_LENGTH) {
          fprintf(stderr, "Read too long\n");
          exit(1);
        }

        read[seq_idx++] = b;
      }

      int day;
      for (day = 0; day < days; day++) {
        if (strncmp(id, metadata + day*ID_LEN, ID_LEN) == 0) {
          break;
        }
      }
      if (day == days) {
        fprintf(stderr, "unrecognized input id %.11s\n", id);
        exit(1);
      }

      handle_read(read, seq_idx, day, map, kmer_include,
                  kmer_exclude);
      seq_idx = 0;
    }
    prev = b;
  }

  for (auto i : map) {
    KMer kmer;
    unpack_kmer(i.first, kmer);
    printf("%." K_STR "s", kmer.data());
    for (int day = 0; day < days; day++) {
      printf("\t%u", i.second.get(day));
    }
    printf("\n");
  }
}
