import re
import math
from itertools import count, chain, product, combinations_with_replacement, islice

# gives us the points to partition a sequence,
# assuming a minimum irreducible size of m
def middle_range(xs,m):
    m = min(len(xs)-1,m)
    middle_start = (len(xs)//2)+1+(-m//2)
    return range(middle_start, middle_start+m)
#
def is_sequenced(d,m,xs):
    if xs in d[0]:
        return True
    if xs in d[1]:
        return False
    m = min(m, len(xs))
    result = any((is_sequenced(d,m,xs[:i]) and is_sequenced(d,m,xs[i:])) for i in middle_range(xs,m))
    d[0].add(xs) if result else d[1].add(result)
    return result

# check if xs can be partitiioned into 2 or more smaller sequences
# m is the maximum size of an irreducible sequence in d.
def is_reducible(d, m, xs):
    m = min(m, len(xs))
    return any((is_sequenced(d,m,xs[:i]) and is_sequenced(d,m,xs[i:])) for i in middle_range(xs,m))


def partitions(d,basic, m, xs):
    if xs in d[1]:
        raise StopIteration
    if xs in basic:
        yield ()
    for i in middle_range(xs,m):
        for left in set(partitions(d,basic,m,xs[:i])):
            for right in set(partitions(d,basic,m,xs[i:])):
                yield (*left,i,*(r+i for r in right))

def count_partitions(solved, basic, m, xs):
    if not xs: return 1
    if xs in solved: return solved[xs]
    m = min(m, len(xs))
    result = sum(count_partitions(solved,basic,m,xs[i:]) for i in range(1,m+1)[::-1] if xs[:i] in basic)
    solved[xs] = result
    return result
        

def part1(towels, patterns):
    d = (set(towels),set())
    m = max(len(t) for t in towels)
    irreducibles = set(t for t in towels if not is_reducible(d,m,t))

    for i in range(1,10+1):
        for xs in combinations_with_replacement('rgbuw', i):
            is_sequenced(d,m,xs)
    sequencable = set(xs for xs in patterns if is_sequenced(d,m,xs))
    print(len(sequencable))
    
def part2(towels, patterns):
    d = (set(towels),set())
    m = max(len(t) for t in towels)
    solved = dict()
    for i in range(1,10+1):
        for xs in combinations_with_replacement('rgbuw', i):
            count_partitions(solved,towels,m,xs)
    print(sum(count_partitions(solved,towels,m,p) for p in patterns))
    
    
def main():
    fname = "day19_input"
    with open(fname, 'r') as f:
        data = [l.strip() for l in f.read().strip().split("\n")]
        k = next(i for i, x in enumerate(data) if not x)    
        towels = tuple(x for l in data[:k] for x in re.findall('\w+',l))
        patterns = tuple(x for l in data[k+1:] for x in re.findall('\w+',l))
        part1(towels, patterns)
        part2(towels, patterns)

if __name__ == "__main__":
    main()
