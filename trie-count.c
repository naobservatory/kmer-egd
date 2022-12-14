#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define K 40
#define K_STR "40"

#define MAX_READ_LENGTH 151
#define DAYS 14

struct TrieNode {
  // If days is set then we're a leaf node; otherwise we're an inner node.  We
  // know which case because the first K nodes will be inner, the last will be
  // a leaf.
  union {
    uint32_t* days;
    struct TrieNode* A;
  };
  struct TrieNode* C;
  struct TrieNode* G;
  struct TrieNode* T;
};

uint64_t memory_used = 0;
void* zmalloc(size_t size) {
  memory_used += size;
  void* m = malloc(size);
  memset(m, 0, size);
  return m;
}

void handle_read(char* read, int read_len, int day, struct TrieNode* root,
                 char* kmer_include, char* kmer_exclude) {
  int poly_g_count = 0;
  for (int i = read_len; i > 0; i--) {
    if (read[i-1] == 'G') {
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

    struct TrieNode* pos = root;
    for(int j = 0; j < K; j++) {
      switch(read[i + j]) {
      case 'A':
        if (pos->A == NULL) pos->A = zmalloc(sizeof(struct TrieNode));
        pos = pos->A;
        break;
      case 'C':
        if (pos->C == NULL) pos->C = zmalloc(sizeof(struct TrieNode));
        pos = pos->C;
        break;
      case 'G':
        if (pos->G == NULL) pos->G = zmalloc(sizeof(struct TrieNode));
        pos = pos->G;
        break;
      case 'T':
        if (pos->T == NULL) pos->T = zmalloc(sizeof(struct TrieNode));
        pos = pos->T;
        break;
      default:
        return;
      }
    }
    if (pos->days == NULL) pos->days = zmalloc(sizeof(uint32_t) * DAYS);
    if (pos->days[day] < UINT32_MAX) {
      pos->days[day]++;
    }
  }
}

void print_trie(struct TrieNode* node, int depth, char kmer[K]) {
  if (node == NULL) {
    return;
  }
  if (depth == K) {
    printf("%." K_STR "s", kmer);
    for (int day = 0; day < DAYS; day++) {
      printf("\t%u", node->days[day]);
    }
    printf("\n");
  } else {
    kmer[depth] = 'A';
    print_trie(node->A, depth+1, kmer);
    kmer[depth] = 'C';
    print_trie(node->C, depth+1, kmer);
    kmer[depth] = 'G';
    print_trie(node->G, depth+1, kmer);
    kmer[depth] = 'T';
    print_trie(node->T, depth+1, kmer);
  }
}

void determine_fullness(struct TrieNode* node, int depth,
                        uint64_t* inner_nodes, uint64_t* leaf_nodes) {
  if (node == NULL) {
    return;
  }
  if (depth == K) {
    (*leaf_nodes)++;
  } else {
    (*inner_nodes)++;
    determine_fullness(node->A, depth+1, inner_nodes, leaf_nodes);
    determine_fullness(node->C, depth+1, inner_nodes, leaf_nodes);
    determine_fullness(node->G, depth+1, inner_nodes, leaf_nodes);
    determine_fullness(node->T, depth+1, inner_nodes, leaf_nodes);
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

  struct TrieNode* root = zmalloc(sizeof(struct TrieNode));

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
      handle_read(read, seq_idx, read_num % DAYS, root, kmer_include,
                  kmer_exclude);
      seq_idx = 0;
      read_num++;
    }
    prev = b;
  }

  fprintf(stderr, "Memory used: %ld bytes\n", memory_used);
  fprintf(stderr, "Printing kmers...\n");

  char kmer[K];
  print_trie(root, /*depth=*/0, kmer);

  //uint64_t inner_nodes = 0;
  //uint64_t leaf_nodes = 0;
  //determine_fullness(root, /*depth=*/0, &inner_nodes, &leaf_nodes);
  //printf("%lu %lu\n", inner_nodes, leaf_nodes); // 364591541 19384822
}
