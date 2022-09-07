import sys

_, mods, mod = sys.argv
mods = int(mods)
mod = int(mod)

for i, line in enumerate(sys.stdin):
    if i % mods == mod:
        sys.stdout.write(line)
        
