CFLAGS=-O3 -Wall -lrt
CC=gcc
OUTPUTS=count-kmer-eqs open-shm close-shm read-shm shm-hist shm-examples \
  extract-kmers test
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

.gitignore:
	echo $(OUTPUTS) | tr ' ' '\n' > .gitignore
	echo /target >> .gitignore
	echo '\#*' >>  .gitignore
	echo '\.#*' >>  .gitignore

.PHONY: clean

clean:
	rm -f $(TARGETS)
