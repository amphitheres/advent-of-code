from itertools import product
from collections import deque

def score_trailhead(trailhead, trailmap):
    component = set([trailhead])
    frontier = deque([trailhead])
    while True:
        try:
            i, j = frontier.pop()
        except IndexError:
            break
        for di, dj in [(1,0),(-1,0),(0,1),(0,-1)]:
            ii,jj = i+di,j+dj
            # In the following two situations, skip this di,dj (using continue)
            if (ii,jj) in component:
                continue
            try:
                x = trailmap[ii,jj]
            except KeyError:
                continue
            # Check if ii,jj can be reached (height increase of 1)
            if x-trailmap[i,j] == 1:
                # add to the connected component and the frontier
                component.add((ii,jj))
                frontier.append((ii,jj))
    return sum((1 for x in component if trailmap[x]==9))
    
def part1(trailheads, trailmap):
    return sum((score_trailhead(t, trailmap) for t in trailheads))
def distinct_trails(trailhead, trailmap, scoremap):
    try:
        return scoremap[trailhead]
    except KeyError:
        pass
    
    if trailmap[trailhead] == 9:
        scoremap[trailhead] = 1
        return 1
    
    i,j = trailhead
    score = 0
    for di, dj in [(1,0),(-1,0),(0,1),(0,-1)]:
        ii,jj = i+di,j+dj
        try:
            if trailmap[ii,jj]-trailmap[trailhead] == 1: 
                score += distinct_trails((ii,jj), trailmap, scoremap)
        except KeyError:
            continue
    scoremap[trailhead] = score
    return score
            
        
    
def part2(trailheads, trailmap):
    scoremap = dict()
    return sum((distinct_trails(t, trailmap, scoremap) for t in trailheads))

def main():
    filename = 'day_10_input'
    with open(filename, 'r') as the_file:

        data = tuple(the_file.readlines())
        trailmap = {(i, j): int(c) for i,line in enumerate(data) for j,c in enumerate(line.strip())}
        trailheads = tuple(coord for coord in trailmap if trailmap[coord] == 0)
        print(part1(trailheads, trailmap))
        print(part2(trailheads, trailmap))

if __name__ == '__main__':
    main()
