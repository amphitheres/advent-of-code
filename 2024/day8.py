import re
import itertools
def main():
    p = re.compile("[a-zA-Z0-9]")
    filename = "day_8_test"
    
    with open(filename, 'r') as the_file:
        data = [list(line.strip()) for line in the_file.readlines()]
        height = len(data)
        width = len(data[0])
        in_bounds = lambda i,j: i>=0 and i<height and j>=0 and j<width
        letters = [x for xs in data for x in xs if p.match(x)]
        antennae = {l:list(set((i,j) for (i,line) in enumerate(data) for (j, x) in enumerate(line) if x == l)) for l in letters}
        # generator to get the antinodes for part 1
        def antinodes(xs):
            pairs = itertools.product(xs,xs)
            for ((i1,j1),(i2,j2)) in pairs:
                if i1==i2 and j1==j2:
                    continue
                yield (2*i1-i2,2*j1-j2)
                yield (2*i2-i1,2*j2-j1)
        for xs in data:
            print(''.join(xs))
        data_copy = [xs[:] for xs in data]

        all_antinodes = set(x for xs in antennae.values() for x in antinodes(xs) if in_bounds(*x))
        print(all_antinodes)
        for (i,j) in all_antinodes:
            data_copy[i][j]='#'
        print("Antinodes")
        for xs in data_copy:
            print(''.join(xs))
        print(len(all_antinodes))
        # new generator for antinodes in part 2
        def extra_antinodes(xs):
            pairs = itertools.product(xs,xs)
            for ((i1,j1),(i2,j2)) in pairs:
                if i1==i2 and j1==j2:
                    continue
                vx = i1-i2
                vy = j1-j2
                x = i1
                y = j1
                while in_bounds(x,y):
                    yield (x,y)
                    x+=vx
                    y+=vy
                x = i2
                y = j2
                while in_bounds(x,y):
                    yield (x,y)
                    x-=vx
                    y-=vy
        
        all_extra_antinodes = set(x for xs in antennae.values() for x in extra_antinodes(xs))
        print(len(all_extra_antinodes))
                    
if __name__ == "__main__":
    main()
