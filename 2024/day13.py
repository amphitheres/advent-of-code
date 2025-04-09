import re
from itertools import count, takewhile
from functools import reduce

def part1(machines_and_prizes):
    print(sum(cost(*x) for x in machines_and_prizes))

def cost(ax, ay, bx, by, px, py):
    # A = (ax bx
    #      ay by)
    # det(A) = ax*by-ay*bx
    # A^(-1) = (1/det(A)) *(by -bx
    #                       -ay ax)
    detA = ax*by-ay*bx
    if detA:
        detAza = by*px + (-bx*py)
        detAzb = (-ay*px) + ax*py
        return 0 if detAza % detA | detAzb % detA else 3*(detAza//detA) + (detAzb//detA)
    else:
        # det(A) was zero, implying columns a and b are linearly dependent.
        # Check if px,py is a scalar multiple of a. If it is not, return 0.
        if ax*py - px*ay:
            return 0
        # Either it is a scalar multiple of a or b or neither
        # make a list of costs between a and b.
        costa = 0 if px % ax else 3*(px//ax)
        costb = 0 if px % bx else px//bx
        try:
            # return the minimum of non-zero costs if possible.
            return min(i for i in (costa, costb) if i)
        except ValueError:
            return 0
def part2(machines_and_prizes):
    alter = lambda ax,ay,bx,by,px,py: (ax,ay,bx,by,px+10000000000000,py+10000000000000)
    print(sum(cost(*(alter(*x))) for x in machines_and_prizes))
        
def main():
    filename = "day_13_input"
    with open(filename, 'r') as f:
        data = tuple(l for l in map(str.strip,f.readlines()) if l)
        extract = lambda xss: tuple(int(x) for xs in xss for x in re.findall('\d+',xs))
        machines_and_prizes = tuple(extract(data[i:i+3]) for i in range(0,len(data),3))
        part1(machines_and_prizes)
        part2(machines_and_prizes)
        

if __name__ == "__main__":
    main()
