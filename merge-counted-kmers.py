import sys

DONE='Z'  # sorts after all kmers

def to_key(row):
    return row.split('\t')[0]

def to_count(row):
    return int(row.split('\t')[-1])

fnames = sys.argv[1:]
files = [open(fname) for fname in fnames]
nexts = [next(f) for f in files]

while True:
    count = 0
    key = min([to_key(row) for row in nexts])
    if key == DONE:
        break
    
    for i in range(len(fnames)):
        if nexts[i] == DONE: continue
        try:
            while to_key(nexts[i]) == key:
                count += to_count(nexts[i])
                nexts[i] = next(files[i])
        except StopIteration:
            nexts[i] = DONE

    print('%s\t%s' % (key, count))
    
    
