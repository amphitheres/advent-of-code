import math
from collections import deque
from itertools import chain

def score(d, dd):
    dot = d.imag*dd.imag + d.real*dd.real
    if dot == 1:
        return 1
    elif dot == -1:
        return 2001
    else:
        return 1001
def neighbours(r,dr,vertices):
    a = ((r+dr,dr),1)
    bs = (((r,dr*x),1000) for x in (1j,-1j))
    c = ((r,-dr),2000)
    return ((v,s) for v,s in (a,*bs,c) if v in vertices)

def part1(vertices, start, end):
    # Djikstra's algorithm to find shortest path
    # https://en.wikipedia.org/wiki/Dijkstra's_algorithm
    dist = {}
    prev = {}
    dist[start] = 0
    
    unprocessed = set(vertices)
    # this should be equal to set(dist) & Q at the end of each loop.
    frontier = set([start])
    
    while frontier:
        v = min(frontier, key=dist.get)
        unprocessed.remove(v)
        frontier.remove(v)
        
        for u,s in neighbours(*v,unprocessed):
            dist_u = dist.get(u,math.inf)
            new_dist_u = s + dist[v]
            if new_dist_u <= dist_u:
                dist[u] = new_dist_u
                if new_dist_u == dist_u:
                    prev[u] = prev.get(u,[]) + [v]
                else:
                    prev[u] = [v]
                frontier.add(u)
    print(min(dist.get((end,dr),math.inf) for dr in (1,-1,1j,-1j)))

def generate_paths(prev, v):
    try:
        return (chain([v],path) for u in prev[v] for path in generate_paths(prev, u))
    except KeyError:
        return [[v]]
    
def part2(vertices, start, end):
    # Djikstra's algorithm to find shortest path
    # https://en.wikipedia.org/wiki/Dijkstra's_algorithm
    dist = {}
    prev = {}
    dist[start] = 0
    
    unprocessed = set(vertices)
    # this should be equal to (set(dist) & unprocessed) at the end of each loop.
    frontier = set([start])
    
    while frontier:
        v = min(frontier, key=dist.get)
        unprocessed.remove(v)
        frontier.remove(v)
        
        for u,s in neighbours(*v,unprocessed):
            dist_u = dist.get(u,math.inf)
            new_dist_u = s + dist[v]
            if new_dist_u <= dist_u:
                dist[u] = new_dist_u
                if new_dist_u == dist_u:
                    prev[u] = prev.get(u,[]) + [v]
                else:
                    prev[u] = [v]
                frontier.add(u)
    min_dist = min(dist[end,d] for d in (1,-1,1j,-1j))
    endpoints = [(end, d) for d in (1,-1,1j,-1j) if dist[end,d] == min_dist]
    print(endpoints)
    best_possible_paths = [list(path) for path in chain.from_iterable(generate_paths(prev, v) for v in endpoints)]
    print(best_possible_paths)
    print("there are",len(best_possible_paths), "best possible paths")
    print(len(set(r for path in best_possible_paths for r,dr in path)))
    
def main():
    fname = "day_16_input"
    with open(fname, 'r') as f:
        data = tuple(f.read().split('\n'))
        
        charmap = {(i+1j*j):c for i,l in enumerate(data) for j,c in enumerate(l) if c !='#'}
        vertices = set((r,dr) for r in charmap for dr in (1,-1,1j,-1j))
        start = next(r for r,_ in vertices if charmap[r] == 'S')
        end = next(r for r,_ in vertices if charmap[r] == 'E')

        part1(vertices, (start,1j), end)
        part2(vertices, (start,1j), end)
    


if __name__ == "__main__":
    main()
