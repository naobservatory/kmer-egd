#ifndef UTIL_H
#define UTIL_H

#include <stdio.h>

// HashGenomicCircularBuffer assumes K & 3 == 0
#define K 40
#define K_STR "40"

#define INITIAL 0
#define GOT_AT 1
#define IN_SEQ 2

// kmer and kmer_rc are both K long
typedef void (*kmer_handler_t)(char* circular_buffer, int offset, void *data);

void iterate_kmers(kmer_handler_t kmer_handler, void* data) {
  char b;
  int state = INITIAL;
  int seq_idx = 0;

  char circular_buffer[K];

  while ((b = getchar_unlocked()) != EOF) {
    if (state == IN_SEQ && b != '\n' && b != '+') {
      int beginning = seq_idx - K + 1;
      int end = seq_idx % K;
      circular_buffer[end] = b;

      if (beginning >= 0) {
        // We have a complete K-mer to work with.
        kmer_handler(circular_buffer, beginning % K, data);
      }
      
      seq_idx++;
    }

    if (state == INITIAL && b == '@') {
      state = GOT_AT;
    } else if (state == GOT_AT && b == '\n') {
      state = IN_SEQ;
      seq_idx = 0;
    } else if (state == IN_SEQ && b == '+') {
      state = INITIAL;
    }
  }
}

#endif // UTIL_H
