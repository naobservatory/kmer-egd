#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>

// sequences can't be longer than this
#define BUFSIZE 1024
#define K 40

#define BASE_A 0
#define BASE_C 1
#define BASE_G 2
#define BASE_T 3
#define BASE_N 4
#define N_BASES 5

#define MISMATCH_PENALTY 0.9

int to_base_enum(char base) {
  switch(base) {
  case 'A': return BASE_A;
  case 'C': return BASE_C;
  case 'G': return BASE_G;
  case 'T': return BASE_T;
  default: return BASE_N;
  }
}

double score(const char* contig,
             size_t contig_len,
             const char* seq,
             size_t seq_len,
             size_t match_pos,
             int direction) {
  int matches = K;
  int mismatches = 0;

  int contig_index = direction == 1 ? K :contig_len-K-1;
  int seq_index = direction == 1 ? match_pos + K : match_pos - 1;

  while (0 <= contig_index && contig_index < contig_len &&
         0 <= seq_index && seq_index < seq_len) {
    if (contig[contig_index] == seq[seq_index]) {
      matches += 1;
    } else {
      mismatches += 1;
    }
    contig_index += direction;
    seq_index += direction;
  }
  return matches * pow(MISMATCH_PENALTY, mismatches);
}  

int main(int argc, const char** argv) {
  if (argc != 3) {
    printf("usage: cat seqs | %s <n|p> <contig>\n", argv[0]);
    exit(1);
  }
  const int want_next = argv[1][0] == 'n';
  const char* contig = argv[2];
  const int contig_len = strlen(contig);

  char needle[K+1];
  if (want_next) {
    for (int i = 0; i < K; i++) {
      needle[i] = contig[contig_len - K + i];
    }
  } else {
    for (int i = 0; i < K; i++) {
      needle[i] = contig[i];
    }
  }
  needle[K] = '\0';

  double counts[N_BASES];

  char buf[BUFSIZE];
  const char* seq;
  while ((seq = fgets(buf, BUFSIZE, stdin)) != NULL) {
    char* match = strstr(seq, needle);
    if (match == NULL) continue;

    size_t match_pos = match - seq;

    int seq_len = strlen(seq) - 1; // ignore trailing newline

    if (want_next) {
      size_t end_pos = match_pos + K;
      if (end_pos < seq_len) {
        counts[to_base_enum(seq[end_pos])] +=
          score(contig, contig_len, seq, seq_len, match_pos, -1);
      }
    } else {
      size_t start_pos = match_pos - 1;
      if (start_pos >= 0) {
        counts[to_base_enum(seq[start_pos])] +=
          score(contig, contig_len, seq, seq_len, match_pos, 1);
      }
    }
  }

  printf("%f\t%f\t%f\t%f\n",
         counts[BASE_A], counts[BASE_C], counts[BASE_G], counts[BASE_T]);
}
