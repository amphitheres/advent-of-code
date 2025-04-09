from itertools import product
from functools import reduce
def pin_heights(s):
    k = s.split('\n')
    w,h = len(k[0]), len(k)
    return tuple(sum(1 for i in range(h) if k[i][j]=='#')-1 for j in range(w))

def parse_input(fname):
    with open(fname, 'r') as f:
        keys_and_locks = tuple(l.strip() for l in f.read().split('\n\n'))
        keys = tuple(pin_heights(x) for x in keys_and_locks if x[0]=='.')
        locks = tuple(pin_heights(x) for x in keys_and_locks if x[0]=='#')
        return keys, locks

def part1(keys, locks):
    keys = frozenset(keys)
    locks = frozenset(locks)
    print("keys:",len(keys))
    print("locks:",len(locks))
    compatible = lambda xs,ys: all(x+y<=5 for x,y in zip(xs,ys))
    print("unique pairs:", sum(compatible(xs,ys) for xs,ys in product(keys, locks)))
    

def main():
    fname = "day25_input"
    keys, locks = parse_input(fname)
    part1(keys, locks)


if __name__ == "__main__":
    main()
