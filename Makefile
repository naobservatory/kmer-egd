all: count-kmer-eqs open-shm close-shm read-shm

count-kmer-eqs: count-kmer-eqs.c superfasthash.h
	gcc count-kmer-eqs.c -O2 -o count-kmer-eqs -Wall

open-shm: open-shm.c shm-common.h
	gcc open-shm.c -O2 -o open-shm -Wall

close-shm: close-shm.c shm-common.h
	gcc close-shm.c -O2 -o close-shm -Wall

read-shm: read-shm.c shm-common.h
	gcc read-shm.c -O2 -o read-shm -Wall
