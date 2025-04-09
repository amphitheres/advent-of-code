import re
from functools import reduce
from operator import mul
from collections import Counter

def print_grid(guards, w, h):
    mid_h = h//2
    mid_w = w//2
    counted_guards = Counter(guards)
    grid_w_guards = [[str(counted_guards[j,i]) if (j,i) in counted_guards else '.' for j in range(w)] for i in range(h)]
    print('\n'.join([''.join(row) for row in grid_w_guards]))

def part1(data, w, h):
    mid_w = w//2
    mid_h = h//2
    seconds = 100
    update = lambda px,py,vx,vy,n: ((px + n*vx) % w, (py + n*vy) % h)
    updated_guards = [update(*guard,seconds) for guard in data]
    quadrants = ((abs(px-1)//mid_w,abs(py-1)//mid_h) for px,py in updated_guards if px!=mid_w and py!=mid_h)
    print(reduce(mul, Counter(quadrants).values(), 1))
    
def part2(data,w,h):
    update = lambda px,py,vx,vy,n: ((px + n*vx) % w, (py + n*vy) % h)
    k = 10
    top_w = w//k
    top_h = h//k
    # I didn't know what kind of image to expect for part 2, so I tried searching for advent of code christmas tree
    # and day 14 christmas tree just in case this was a reference to some previous AoC problem.
    # Well "image compression" was mentioned in some of the results. Spoiled the solution a bit, but gave me an idea.
    # I tried reusing the same sort of entropy measurement from part 1
    # except I divide the grid into k x k sized rectangles instead of w//2 x h//2 sized rectangles
    entropy = lambda i: reduce(mul,Counter((px//k,py//k) for px,py in (update(*g,i) for g in data)).values(),1)
    # sort the possible grids by their entropy, hopefully the first one is the tree
    filtered_seconds = sorted(range(w*h), key=entropy)
    print("Searching", len(filtered_seconds), "possible results, ordered by least entropy.")
    # interactively print the ones from the filtered list
    for i in filtered_seconds:
        updated_guards = [update(*g,i) for g in data]
        print_grid(updated_guards, w, h)
        x = input("%d seconds elapsed. Enter 'q' to end: " % (i))
        if x == 'q':
            break
        

def main():
    # w = 11
    # h = 7
    w,h=101,103
    fname = "day_14_input"
    with open(fname, 'r') as f:
        data = tuple(tuple(int(x) for x in re.findall('-?\d+',l)) for l in f.readlines())
        part1(data, w, h)
        part2(data, w, h)

if __name__ == "__main__":
    main()
