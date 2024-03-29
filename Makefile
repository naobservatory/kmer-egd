CFLAGS=-O3 -Wall -lrt -lm -Werror
CPPFLAGS=-O3 -Wall -lrt -lm -Werror
CC=gcc
OUTPUTS=count-kmer-eqs open-shm close-shm read-shm shm-hist shm-examples \
  extract-kmers test shm-egd shm-dump-all trie-count fasta-to-ecs hash-count \
  ska-hash-count hash-count-variable hash-count-union hash-count-single \
  hash-count-rothman iterative-assembler
TARGETS=$(OUTPUTS) .gitignore

all: $(TARGETS)

count-kmer-eqs: count-kmer-eqs.c superfasthash.h util.h shm-common.h

test: test.c superfasthash.h util.h

extract-kmers: extract-kmers.c superfasthash.h util.h

open-shm: open-shm.c shm-common.h

close-shm: close-shm.c shm-common.h

read-shm: read-shm.c shm-common.h

shm-hist: shm-hist.c shm-common.h

shm-examples: shm-examples.c shm-common.h

shm-egd: shm-egd.c shm-common.h

shm-dump-all: shm-dump-all.c

trie-count: trie-count.c

hash-count: hash-count.cpp

hash-count-variable: hash-count-variable.cpp

hash-count-union: hash-count-union.cpp

hash-count-rothman: hash-count-rothman.cpp

hash-count-single: hash-count-single.cpp

ska-hash-count: ska-hash-count.cpp

fasta-to-ecs: fasta-to-ecs.c

iterative-assembler: iterative-assembler.c

.gitignore:
	echo $(OUTPUTS) | tr ' ' '\n' > .gitignore
	echo /target >> .gitignore
	echo '\#*' >>  .gitignore
	echo '\.#*' >>  .gitignore
	echo '*.tsv' >>  .gitignore
	echo '*.min-p' >>  .gitignore
	echo 'SRR*.fasta' >>  .gitignore
	echo '*tmp.*' >>  .gitignore
	echo "bucket-evaluations*.tsv" >> .gitignore
	echo "prjna729801.fnames.partitioned" >> .gitignore
	echo "__pycache__" >> .gitignore
	echo '*.log' >> .gitignore


.PHONY: clean

.DELETE_ON_ERROR:

clean:
	rm -f $(TARGETS)
