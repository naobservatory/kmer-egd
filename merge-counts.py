import sys

DONE='Z'  # sorts after all kmers

def to_key(row):
    if row == DONE: return DONE
    return row.split('-')[0]

def to_day(row):
    return int(row.split('-')[1].split('\t')[0])

def to_count(row):
    return int(row.split('\t')[-1])

fnames = sys.argv[1:]
files = [open(fname) for fname in fnames]
nexts = [next(f) for f in files]

DAYS=14

while True:
    cur = [0]*DAYS
    key = min([to_key(row) for row in nexts])
    if key == DONE:
        break
    
    for i in range(len(fnames)):
        if nexts[i] == DONE: continue
        try:
            while to_key(nexts[i]) == key:
                cur[to_day(nexts[i])] += to_count(nexts[i])
                nexts[i] = next(files[i])
        except StopIteration:
            nexts[i] = DONE

    print('\t'.join([key] + [str(x) for x in cur]))
    
    
