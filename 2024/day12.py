from collections import deque

def distinct_neighbours(i, j, cropmap):
    # compass directions, north, west, east, south
    deltas = tuple((i,j) for i in (-1,0,1) for j in (-1,0,1) if bool(i)^bool(j))
    c = cropmap[i,j]
    acc = 0
    for di,dj in deltas:
        try:
            if cropmap[i+di,j+dj]!=c:
                acc+=1
        except KeyError:
            acc+=1
    return acc
        
def mark_region(i, j, regionmap, cropmap):
    # return early if this region already marked
    try:
        return regionmap[i,j]
    except KeyError:
        pass
    # compass directions, north, west, east, south
    deltas = tuple((i,j) for i in (-1,0,1) for j in (-1,0,1) if bool(i)^bool(j))
    region = set()
    c = cropmap[i,j]
    frontier = deque([(i,j)])
    while True:
        try:
            i,j = frontier.pop()
        # End condition of loop
        except IndexError:
            break
        try:
            if cropmap[i,j] == c:
                region.add((i,j))
                regionmap[i,j] = region
                frontier.extend((i+di,j+dj) for di,dj in deltas if (i+di,j+dj) not in region)
        except KeyError:
            pass
        
    return region

def part1(cropmap):
    regionmap = dict()
    # each region is identified with its minimum coordinate (ordered lexicographically)
    regions = set(min(mark_region(*key,regionmap,cropmap)) for key in cropmap)
    perimeter = lambda r: sum(distinct_neighbours(i,j,cropmap) for i,j in regionmap[r])
    area = lambda r: len(regionmap[r])          
    print(sum(area(r)*perimeter(r) for r in regions))

def count_sides(region, cropmap):
    # compass directions, north, west, east, south
    deltas = tuple((i,j) for i in (-1,0,1) for j in (-1,0,1) if bool(i)^bool(j))
    def is_side(i,j,di,dj):
        try:
            return cropmap[i,j]!=cropmap[i+di,j+dj]
        except KeyError:
            return True
    # count the number of sides separately with respect to each direction
    count = 0
    for dx in deltas:
        side_cropmap = {x:cropmap[x] for x in region if is_side(*x,*dx)}
        side_regionmap = dict()
        side_regions = set(min(mark_region(*key,side_regionmap,side_cropmap)) for key in side_cropmap)
        count += len(side_regions)
    return count

def part2(cropmap):
    # similar to part1, except we use a different perimeter function.
    regionmap = dict()
    regions = set(min(mark_region(*key,regionmap,cropmap)) for key in cropmap)
    perimeter = lambda r: count_sides(regionmap[r], cropmap)
    area = lambda r: len(regionmap[r])
    
    print(sum(area(r)*perimeter(r) for r in regions))

    
def main():
    file_name = "day_12_input"
    with open(file_name, 'r') as the_file:
        data = tuple(line.strip() for line in the_file.readlines())
        cropmap = {(i,j):c for i,x in enumerate(data) for j,c in enumerate(x)}
        part1(cropmap)
        part2(cropmap)
        
        

if __name__ == "__main__":
    main()
