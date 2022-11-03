import sys
buckets, = sys.argv[1:]
buckets = int(buckets)

data = [line.strip() for line in sys.stdin]
for i in range(buckets):
    print("%s\t%.3f%%" % (data[i*len(data)//buckets], i/buckets*100))
    
