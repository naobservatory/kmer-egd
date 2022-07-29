#include <stdlib.h>
#include "util.h"
#include "superfasthash.h"

const char* sq1 = "AGACCCGGGAACGTATTCACCGCGACATGCTGATCCTGTC";
const char* rc1 = "GACAGGATCAGCATGTCGCGGTGAATACGTTCCCGGGTCT";

const char* sq2 = "GTCAGACCCGGGAACGTATTCACCGCGACATGCTGATCCT";

const char* fw_seq =
  "GGTGAAATCCTGCCGCTTAACGGTAGAATTGCCATTGATACTGAAAAGCTTCTGTCTCTTATACACATCTG"
  "ACGCTGCCGACGATGTCGCTGGTGGGTTGATCTAGGGGGTGGGCGGATGATTAAATAGGGGGGGGGGGGGG";
const char* rc_seq =
  "CCCCCCCCCCCCCCTATTTAATCATCCGCCCACCCCCTAGATCAACCCACCAGCGACATCGTCGGCAGCGT"
  "CAGATGTGTATAAGAGACAGAAGCTTTTCAGTATCAATGGCAATTCTACCGTTAAGCGGCAGGATTTCACC";
#define LEN_SEQ (142)

int main(int argc, char** argv) {
  uint64_t h1, h2;
  for (int offset = 0 ; offset < K ; offset++) {
    h1 = HashGenomicCircularBuffer(sq1, offset);
    h2 = HashGenomicCircularBuffer(sq2, (offset + 3) % K);
    if (h1 != h2) {
      printf("Offset mishandled: %s %s %d %lu %lu\n",
             sq1, sq2, offset, h1, h2);
      exit(1);
    }
  }

  h1 = HashGenomicCircularBuffer(sq1, 0);
  h2 = HashGenomicCircularBuffer(rc1, 0);
  if (h1 != h2) {
    printf("RC mishandled: %s %s %lu %lu", sq1, rc1, h1, h2);
  }

  char buf_f[K];
  char buf_r[K];
  
  for (int i = 0 ; i < LEN_SEQ; i++) {
    buf_f[i % K] = fw_seq[i];
    buf_r[i % K] = rc_seq[i];

    int beginning = i - K + 1;
    if (beginning < 0) continue;
    int offset = beginning % K;    

    h1 = HashGenomicCircularBuffer(buf_f, offset);
    h2 = HashGenomicCircularBuffer(buf_r, offset);

    printf("F\t%lu\t", h1);
    for (int j = offset; j < K; j++) {
      printf("%c", buf_f[j]);
    }
    for (int j = 0; j < offset; j++) {
      printf("%c", buf_f[j]);
    }
    printf("\n");
    
    printf("R\t%lu\t", h2);
    for (int j = offset; j < K; j++) {
      printf("%c", buf_r[j]);
    }
    for (int j = 0; j < offset; j++) {
      printf("%c", buf_r[j]);
    }
    printf("\n");
  }
}
