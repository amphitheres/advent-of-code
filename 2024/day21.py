from collections import deque
from functools import reduce

def pairwise(it, a=None):
    it = iter(it)
    if a is None:
        a = next(it)
    for b in it:
        yield (a,b)
        a=b
    
from itertools import chain
from day18 import djikstra
import re

def prev_to_paths(prev, u):
    if not prev.get(u):
        yield (u,)
        return
    for w in prev[u]:
        for path in prev_to_paths(prev, w):
            yield (*path,u)

def prev_path_to_str(vertex_map, arrows, path):
    xs = [vertex_map[p] for p in path]
    return ''.join([arrows[x-y] for x,y in zip(xs[1:],xs[:-1])]) + 'A'
            
def shortest_paths(vertices, neighbours):
    D = {}
    for v in vertices:
        _,prev = djikstra(vertices, neighbours, v)
        for u in vertices:
            D[v,u] = list(prev_to_paths(prev, u))
    return D

def shortest_paths_str(vertex_map, neighbours, arrows):
    D = shortest_paths(vertex_map, neighbours)
    for k in D:
        prev_paths = D[k]
        D[k] = [prev_path_to_str(vertex_map, arrows, p) for p in prev_paths]
    return D

def shortest_dists(vertices, neighbours):
    D = {}
    for v in vertices:
        dist,_ = djikstra(vertices, neighbours, v)
        for u in vertices:
            D[v,u] = dist[u]
    return D

def to_robot(vertex_map, shortest, arrows, xs, start='A'):
    if len(xs) <= 0:
        yield ''
        return
    end,*xss = xs
    for left in shortest[start, end]:
        for right in to_robot(vertex_map, shortest, arrows, xss, end):
            yield left + right
def to_robot_lazy(vertex_map, shortest, arrows, xs, start='A'):
    return (c for x in pairwise(xs, start) for c in (shortest[x][0]))

def shortest_robot_count(counts, n, xs, start='A'):
    return sum(counts[x,n] for x in pairwise(xs,start))

def shortest_robot(dists, xs, start = 'A'):
    if len(xs) <= 0:
        return 0
    end, *xxs = xs
    return dists[start, end] + 1 + shortest_robot(dists, xxs, end)

def minima(m, xs, key=lambda x:x):
    S = [m]
    km = key(m)
    for x in xs:
        kx = key(x)
        if kx < km:
            S = [x]
            m,km = x,kx
        elif km == kx:
            S.append(x)
    return S
def reduce_robot(vertex_map, rvertex_map, rarrows, xs, start='A'):
    acc = ''
    cursor = vertex_map[start]
    for x in xs:
        if x == 'A':
            acc += rvertex_map[cursor]
        else:
            cursor += rarrows[x]
    return acc

# return -1 if xs < ys, 0 if xs == ys, 1 if xs > ys
def shortest_robot_n(arrowpad, arrows, arrowpad_dists, arrowpad_shortest, xs, n):

    measure_robot = lambda xs: shortest_robot(arrowpad_dists,xs)
    
    robot_iter_a = to_robot(arrowpad, arrowpad_shortest, arrows, xs)
    robot_a = minima(next(robot_iter_a), robot_iter_a, measure_robot)

    for i in range(n):
        robot_iter_a = (x for r in robot_a for x in to_robot(arrowpad, arrowpad_shortest, arrows, r))
        robot_a = minima(next(robot_iter_a), robot_iter_a, measure_robot)
    return measure_robot(robot_a[0])

def prune_shortests(vertices, shortests, key=lambda x: x):
    for v in vertices:
        for u in vertices:
            x, *xs = shortests[v,u]
            shortests[v,u] = minima(x, xs, key)
    return shortests
    
def part1(pins):
    keypad = {'7':0, '8':0+1j, '9':0+2j,
              '4':1, '5':1+1j, '6':1+2j,
              '1':2, '2':2+1j, '3':2+2j,
              '0':3+1j, 'A':3+2j}
    
    arrowpad = {'^':0+1j, 'A':0+2j,
                '<':1,'v':1+1j, '>':1+2j}
    arrows = {0:'',1:'v',-1:'^',-1j:'<',1j:'>'}
    
    rarrows = dict((y,x) for x,y in arrows.items())
    rarrowpad = dict((y,x) for x,y in arrowpad.items())
    rkeypad = dict((y,x) for x,y in keypad.items())

    keypad_neighbours = lambda v: ((rkeypad.get(keypad[v]+dv),1) for dv in (1,-1,1j,-1j))
    arrowpad_neighbours = lambda v: ((rarrowpad.get(arrowpad[v]+dv),1) for dv in (1,-1,1j,-1j))

    arrowpad_shortest = shortest_paths_str(arrowpad, arrowpad_neighbours, arrows)
    keypad_shortest = shortest_paths_str(keypad, keypad_neighbours, arrows)

    arrowpad_dists = shortest_dists(arrowpad, arrowpad_neighbours)
    keypad_dists = shortest_dists(keypad, keypad_neighbours)

    # shortest_robot_n(arrowpad, arrows, arrowpad_dists, arrowpad_shortest, xs, n)
    measure_robot = lambda xs,n: shortest_robot_n(arrowpad, arrows, arrowpad_dists, arrowpad_shortest, xs, n)
    print_test = lambda xs: print(sum(len(i) for i in xs.values()))
    prune_shortests(keypad, keypad_shortest, lambda x: measure_robot(x,1))
    
    prune_shortests(arrowpad, arrowpad_shortest, lambda x: measure_robot(x,1))
    prune_shortests(keypad, keypad_shortest, lambda x: measure_robot(x,2))
    prune_shortests(arrowpad, arrowpad_shortest, lambda x: measure_robot(x,2))
    prune_shortests(keypad, keypad_shortest, lambda x: measure_robot(x,4))
    n = 25
    count_robot = dict()
    for x in keypad_shortest:
        r = keypad_shortest[x][0]
        count_robot[x,0] = len(r)
        for i in range(1,13):
            r = ''.join(to_robot_lazy(arrowpad, arrowpad_shortest, arrows, r))
            count_robot[x,i] = len(r)
    
    for x in arrowpad_shortest:
        r = arrowpad_shortest[x][0]
        count_robot[x,0] = len(r)
        for i in range(1,13):
            r = ''.join(to_robot_lazy(arrowpad, arrowpad_shortest, arrows, r))
            count_robot[x,i] = len(r)
    
    digits = lambda s: int(re.search('\d+',s)[0])
    acc = 0
    print('n',n)
    for pin in pins:
        print(pin)
        robot = ''.join(next(to_robot(keypad, keypad_shortest, arrows, pin)))
        for i in range(n//2):
            robot = ''.join(to_robot_lazy(arrowpad,arrowpad_shortest,arrows, robot))
        acc += shortest_robot_count(count_robot, n//2-1+(n&1), robot, start='A')*digits(pin)
    print(acc)
    
    

def main():
    fname = "day21_input"
    with open(fname, 'r') as f:
        data = tuple(l.strip() for l in f.read().strip().split('\n'))
        part1(data)

if __name__ == "__main__":
    main()
