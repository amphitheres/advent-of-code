import re, math
from collections import deque
def djikstra(vertices, neighbours, start, is_end=(lambda _: False)):
    dist, prev = {start:0}, dict()
    unprocessed = set(vertices)
    frontier = {start}
    while frontier:
        v = min(frontier, key=dist.get)
        if is_end(v):
            return dist, prev
        unprocessed.remove(v)
        frontier.remove(v)
        
        for u,s in neighbours(v):
            if u not in unprocessed: continue
            dist_u = dist.get(u,math.inf)
            new_dist_u = s + dist[v]
            if new_dist_u <= dist_u:
                dist[u] = new_dist_u
                if new_dist_u == dist_u:
                    prev[u] = prev.get(u,[]) + [v]
                else:
                    prev[u] = [v]
                frontier.add(u)
    return dist, prev

def part1(data, m):
    w = max(int(x.real) for x in data)+1
    h = max(int(y.imag) for y in data)+1
    vertices = set(complex(i,j) for i in range(w) for j in range(h))-set(data[:m])
    # Djikstra
    neighbours = lambda v:((v+d,1) for d in (1,-1,1j,-1j))
    start, end = 0j, w-1+1j*(h-1)
    dist, prev = djikstra(vertices, neighbours, start, lambda x: x==end)
    print(dist[end])

def dfs(vertices, neighbours, start, is_end=lambda _:False):
    stack = deque([neighbours(start)])
    discovered = set([start])
    while stack:
        try:
            w,_ = next(stack[0])
            if is_end(w):
                discovered.add(w)
                return discovered, w
            if w in vertices and w not in discovered:
                discovered.add(w)
                stack.appendleft(neighbours(w))
        except StopIteration:
            stack.popleft()
    return discovered, None

def bfs(vertices, neighbours, start, is_end=lambda _:False):
    discovered = {start}
    Q = deque([(start,tuple())])
    while Q:
        v,vs = Q.pop()
        if is_end(v):
            return discovered,(v,vs)
        for w,_ in neighbours(v):
            if w in vertices and w not in discovered:
                discovered.add(w)
                Q.appendleft((w,(v,vs)))
    return discovered,None
    
def part2(data, m):
    w = max(int(x.real) for x in data)+1
    h = max(int(y.imag) for y in data)+1
    vertices = set(complex(i,j) for i in range(w) for j in range(h))-set(data[:m])
    print(len(data))
    neighbours = lambda v:((v+d,1) for d in (1,-1,1j,-1j))
    start, end = 0j, w-1+1j*(h-1)
    for i,v in enumerate(data[m:]):
        vertices.remove(v)
        discovered,_ = bfs(vertices, neighbours, start, lambda x: x==end)
        if end not in discovered:
            print(','.join(str(int(x)) for x in [v.real,v.imag]))
            break
    

def main():
    digits = re.compile('\d+')
    fname,m = "day_18_input",1024
    with open(fname, 'r') as f:
        extract_complex = lambda l: complex(*map(int,digits.findall(l)))
        data = tuple(extract_complex(l) for l in f.read().strip().split('\n'))

        part1(data,m)
        part2(data,m)
        

if __name__ == "__main__":
    main()
