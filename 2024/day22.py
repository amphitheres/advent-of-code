import re
from operator import sub
from functools import reduce
from itertools import accumulate, count, islice, starmap, takewhile, repeat, tee
from collections import deque
M = (1<<24)-1

def pairwise(it):
    a = next(it)
    for b in it:
        yield a,b
        a = b
        
def n_wise(it, n):
    Q = deque(islice(it,n), n)
    yield tuple(Q)
    for x in it:
        Q.append(x)
        yield tuple(Q)

def evolve(s):
    s = ((s<<6)^s)&M
    s = ((s>>5)^s)&M
    s = ((s<<11)^s)&M
    return s

def secrets_generator(s):
    return accumulate(repeat(None),lambda x,_:evolve(x),initial=s)

def prices(s):
    return (x % 10 for x in secrets_generator(s))

def differences(it):
    return starmap(lambda x,y:y-x, pairwise(it))

def sequences_and_prices(s):
    xs, ys = tee(prices(s))
    return zip(n_wise(islice(differences(xs),2000), 4), islice(ys,4,None))
    
def part1(secrets):
    nth_secret = lambda s,n: reduce(lambda x,_: evolve(x),range(n),s)
    n = 2000
    print(sum(map(lambda x: nth_secret(x,n),secrets)))

def part2(secrets):
    totals = dict()
    for s in secrets:
        updates = dict(list(sequences_and_prices(s))[::-1])
        for k in updates:
            totals[k] = totals.get(k,0) + updates[k]
    best_sequence = max(totals,key=totals.get)
    print(totals[best_sequence])
    

def main():
    fname = "day22_input"
    with open(fname, 'r') as f:
        digits = lambda x: int(re.match('\d+',x)[0])
        data = tuple(digits(l) for l in f.read().strip().split('\n'))
        part1(data)
        part2(data)


if __name__ == "__main__":
    main()
        
