from functools import reduce
from operator import add
from collections import deque
# return the amount moved (0 or dr)
def move_tile(grid, r, dr):
    tile = grid.pop(r, '.')
    # base cases
    if tile == '.':
        return dr
    elif tile == '#':
        grid[r] = tile
        return 0
    # Otherwise I am a robot or a box
    # attempt to move what is in front, then move by the returned amount.
    ddr = move_tile(grid, r+dr, dr)
    grid[r+ddr] = tile
    return ddr

def part1(grid_data, r, commands):
    w = max(int(r.imag) for r,_ in grid_data)+1
    h = max(int(r.real) for r,_ in grid_data)+1
    grid = dict(grid_data)
    pp = 100
    for dr in commands:
        r += move_tile(grid, r, dr)
    gps = lambda r: int((r.real)*100+(r.imag))
    print('\n'.join(''.join(grid.get(i+1j*j,'.') for j in range(w)) for i in range(h)))
    print(sum(gps(r) for r,c in grid.items() if c=='O'))


def children(r, dr, grid):
    if dr.imag:
        return [] if grid.get(r+dr,'.') == '.' else [r+dr]

    c = grid.get(r, '.')
    if c == '.':
        return []
    elif c == ']':
        return children(r-1j,dr,grid)
    elif c == '[':
        cc = grid.get(r+dr,'.')+grid.get(r+1j+dr,'.')
        if cc == '[]':
            return [r+dr, r+1j+dr]
        the_children = set([x for x in (r+dr, r+1j+dr) if grid.get(x,'.')!='.'])
        if cc[0] == ']':
            the_children.update([r-1j+dr])
        if cc[1] == '[':
            the_children.update([r+2j+dr])
        return list(the_children)
    else:
        cc = grid.get(r+dr,'.')
        if cc == '.':
            return []
        elif cc == '[':
            return [r+dr, r+1j+dr]
        elif cc == ']':
            return [r+dr, r-1j+dr]
        else:
            return [r+dr]
        
def move_box(r, dr, grid):
    if dr.imag:
        return move_tile(grid,r,dr)
    current_children = set([r])
    stack = deque()
    # check if we can move all obstacles
    while bool(current_children):
        next_children = set()
        for rr in current_children:
            next_children.update(children(rr,dr,grid))
        if '#' in (grid.get(x) for x in next_children):
            return 0
        stack.appendleft(current_children)
        current_children = next_children
    # no obstacles to stop the move, so do it now
    # print(stack)
    for xs in stack:
        for x in xs:
            move_tile(grid,x,dr)
    return dr
    
def part2(grid_data, r, commands):
    
    grid = dict(grid_data)
    w = max(int(r.imag) for r,_ in grid_data)+1
    h = max(int(r.real) for r,_ in grid_data)+1
    # print('\n'.join(''.join(grid.get(i+1j*j,'.') for j in range(w)) for i in range(h)))
    for i,dr in enumerate(commands):
        ddr = move_box(r,dr,grid)
        r+= ddr
        # print("Step %d:" % (i,),dr, dr == ddr, grid.get(r))
        # print('\n'.join(''.join(grid.get(i+1j*j,'.') for j in range(w)) for i in range(h)))
            
    gps = lambda r: int((r.real)*100+(r.imag))
    print(sum(gps(r) for r,c in grid.items() if c =='['))
            
        

def main():
    fname = "day_15_input"
    pt2_test_data = '''##############
##......##..##
##..........##
##....[][]@.##
##....[]....##
##..........##
##############'''.split('\n')
    
    with open(fname,'r') as f:
        data = f.read()
        arrow_to_dr = {'<':-1j,
                       '>':1j,
                       '^':-1,
                       'v':1
                       }
        commands = tuple(arrow_to_dr[x] for x in data if x in arrow_to_dr)
        pt2_test_commands = tuple(arrow_to_dr[x] for x in "<vv<<^^<<^^")
        k = max(i for i,line in enumerate(data.split('\n')) if '#' in line)

        pt1_data = data.split('\n')[:k+1]

        grid_data = lambda d: tuple((i+1j*j,c) for i,l in enumerate(d) for j,c in enumerate(l))
        start = lambda d: next(r for r,c in grid_data(d) if c=='@')
        
        part1(grid_data(pt1_data), start(pt1_data), commands)

        translate = {'.': '..',
                     '@': '@.',
                     '#': '##',
                     'O': '[]'
                     }
        pt2_data = tuple(reduce(add,[translate[c] for c in l],'') for l in pt1_data)
        part2(grid_data(pt2_data), start(pt2_data), commands)

if __name__ == "__main__":
    main()
