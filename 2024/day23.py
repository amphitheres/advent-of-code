import re
from itertools import chain

def get_networks(fname):
    with open(fname) as f:
        networks = re.compile('\w+')
        return (*((*networks.findall(l),) for l in f.read().strip().split('\n')),)
    
def make_networks(data):
    networks = dict()
    for x,y in data:
        try:
            networks[x].add(y)
        except KeyError:
            networks[x] = set([y])
        try:
            networks[y].add(x)
        except KeyError:
            networks[y] = set([x])
    return networks

def biggest_hangout(networks, unprocessed, x):
    def recurse(hangout, mutuals, biggest):
        if len(biggest) < len(hangout):
            biggest = hangout
        for _ in range(len(mutuals)+len(hangout)-len(biggest)):
            y = mutuals.pop()
            if hangout <= networks[y]:
                bigger = recurse(hangout | {y}, mutuals & networks[y], biggest)
                if len(bigger) > len(biggest):
                    biggest = bigger
        return biggest if len(biggest) > len(hangout) else hangout
    return recurse({x},networks[x]&unprocessed, {x})
        
def part1(data):
    networks = make_networks(data)
    triples = set()    
    for netx in networks:
        for nety in networks[netx]:
            netx_and_nety = networks[netx] & networks[nety]
            if netx_and_nety:
                for netz in netx_and_nety:
                    triples.add(frozenset([netx,nety,netz]))
    the_t = frozenset(x for x in networks if x[0]=='t')
    print(sum(1 for t in triples if t & the_t))
                
def part2(data):
    networks = make_networks(data)
    unprocessed = set(networks)
    biggest = set()
    while unprocessed:
        x = unprocessed.pop()
        bigger = biggest_hangout(networks, unprocessed, x)
        print(x, bigger)
        if len(bigger) > len(biggest):
            biggest = bigger
    biggest = list(biggest)
    biggest.sort()
    print("biggest", ','.join(biggest))
    

def main():
    data = get_networks('day23_input')
    part1(data)
    part2(data)
    
if __name__ == "__main__":
    main()
