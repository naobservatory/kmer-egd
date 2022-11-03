import sys
BUCKETS=1000

data = [line.strip() for line in sys.stdin]
for i in range(BUCKETS):
    print("%s\t%.3f%%" % (data[i*len(data)//BUCKETS], i/BUCKETS*100))
    
