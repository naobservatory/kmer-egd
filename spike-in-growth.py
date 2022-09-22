import sys
import random

def randround(val):
    ival = int(val)
    delta = val - ival
    if random.random() < delta:
        return ival + 1
    return ival

def start(days, final, growth):
    # Make the output deterministic
    random.seed(hash((days, final, growth)))

    days = int(days)
    final = int(final)
    growth = 1+float(growth)

    val = final
    out = []
    for _ in range(days):
        out.append(str(randround(val)))
        val /= growth
    out.reverse()
        
    print(" ".join(out))

if __name__ == "__main__":
    start(*sys.argv[1:])
