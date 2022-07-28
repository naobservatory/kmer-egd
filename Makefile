all: count-kmer-eqs open-shm close-shm read-shm shm-hist shm-examples extract-kmers

count-kmer-eqs: count-kmer-eqs.c superfasthash.h util.h
	gcc count-kmer-eqs.c -O2 -o count-kmer-eqs -Wall -lrt

extract-kmers: extract-kmers.c superfasthash.h util.h
	gcc extract-kmers.c -O2 -o extract-kmers -Wall

open-shm: open-shm.c shm-common.h
	gcc open-shm.c -O2 -o open-shm -Wall -lrt

close-shm: close-shm.c shm-common.h
	gcc close-shm.c -O2 -o close-shm -Wall -lrt

read-shm: read-shm.c shm-common.h
	gcc read-shm.c -O2 -o read-shm -Wall -lrt

shm-hist: shm-hist.c shm-common.h
	gcc shm-hist.c -O2 -o shm-hist -Wall -lrt

shm-examples: shm-examples.c shm-common.h
	gcc shm-examples.c -O2 -o shm-examples -Wall -lrt
