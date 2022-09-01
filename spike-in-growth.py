import sys
import random

def start(days, initial, growth):
    days = int(days)
    initial = int(initial)
    growth = 1+float(growth)

    # Make the output deterministic
    random.seed(hash((days, initial, growth)))

    val = initial
    out = []
    for _ in range(days):
        out.append(str(int(val)))
        val *= growth

    print(" ".join(out))

if __name__ == "__main__":
    start(*sys.argv[1:])
