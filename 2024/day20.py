from day18 import djikstra

# return the set of paths in C with taxi distance n
def taxi_paths(n):
    for i in range(1,n//2+(n&1)):
        for u in (1,-1,1j,-1j):
            yield (i+(n-i)*1j)*u
            yield ((i+(n-i)*1j)*u).conjugate()
    for u in (1,-1,1j,-1j):
        yield n*u
    if not(n&1):
        m = n>>1
        for u in (1,-1,1j,-1j):
            yield (m + 1j*m)*u
            
    
    

def part1(track, start, end):

    neighbours = lambda v: ((v+d,1) for d in (1,-1,1j,-1j))
    dist_from_start,_ = djikstra(track, neighbours, start)
    dist_from_end,_ = djikstra(track, neighbours, end)
    
    cheats = lambda v: (v+d for d in taxi_paths(2))
    all_cheats = [(v,u) for v in track for u in cheats(v) if u in track]
    eval_cheat = lambda v,u: dist_from_start[v]+dist_from_end[u]+2
    savings = [(x,dist_from_start[end]-eval_cheat(*x)) for x in all_cheats]
    print(len([x for x,s in savings if s >=100]))
    
def part2(track, start, end):
    neighbours = lambda v: ((v+d,1) for d in (1,-1,1j,-1j))
    
    dist_from_start,_ = djikstra(track, neighbours, start)
    dist_from_end,_ = djikstra(track, neighbours, end)

    cheats = lambda v: ((v+d,n) for n in range(2,21) for d in taxi_paths(n))
    all_cheats = [(v,u,n) for v in track for u,n in cheats(v) if u in track]
    eval_cheat = lambda v,u,n: dist_from_start[v]+dist_from_end[u]+n
    savings = [(x,dist_from_start[end]-eval_cheat(*x)) for x in all_cheats]
    print(len([x for x,s in savings if s >=100]))


def main():
    fname = "day20_input"
    with open(fname, 'r') as f:
        data = tuple((i+1j*j,c) for i,l in enumerate(f.read().strip().split('\n')) for j,c in enumerate(l))
        w = max(int(x.imag) for x,_ in data)+1
        h = max(int(x.real) for x,_ in data)+1
        track = set(x for x,c in data if c!='#')
        start = next(x for x,c in data if c == 'S')
        end = next(x for x,c in data if c == 'E')
        
        part1(track, start, end)
        part2(track, start, end)
        

if __name__ == "__main__":
    main()
