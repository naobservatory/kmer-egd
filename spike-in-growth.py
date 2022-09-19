import sys

def start(days, final, growth):
    days = int(days)
    final = int(final)
    growth = 1+float(growth)

    val = final
    out = []
    for _ in range(days):
        out.append(str(int(val)))
        val /= growth
    out.reverse()
        
    print(" ".join(out))

if __name__ == "__main__":
    start(*sys.argv[1:])
