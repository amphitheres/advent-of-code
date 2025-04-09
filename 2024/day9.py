from functools import reduce
from itertools import cycle, starmap, repeat, count, islice, accumulate
from collections import deque


def main():
    filename = "day_9_input"
    with open(filename, 'r') as the_file:
        data = [int(x) for x in the_file.readline().strip()]

        # Part 1
        nonempty_empty = cycle([lambda i,x: repeat(i//2,x), lambda _,x: repeat(-1,x)])
        disk = [y for ys in (f(*x) for (f,x) in zip(nonempty_empty, enumerate(data))) for y in ys]
        empty_space = (i for i in range(len(disk)) if disk[i] == -1)
        nonempty_space = (i for i in range(len(disk)-1,-1,-1) if disk[i] != -1)
        for (i,j) in zip(empty_space, nonempty_space):
            if j <= i:
                break
            disk[i],disk[j] = disk[j],disk[i]

        checksum = sum(i*x for (i,x) in enumerate(disk) if x != -1)
        print(checksum)
        # Part 2
        # disk2      (id, size, empty_space_after)
        disk2= deque(((i//2, data[i-1], j) for i,j in islice(enumerate(data),1,None,2)))
        if len(data) & 1:
            disk2.append((len(data)//2, data[-1],0))
        
        # i is the id of the current file attempting to move
        max_id = len(disk2)-1
        the_tail = deque()
        
        # walk from the right side of disk2. Pop the element from the end.
        # Compare it to each of the left elements, walking from the left side of disk2.
        # if a left element has enough space after it to fit the right element:
        #     Insert the right element after that left element.
        #     Give the right element a space = space of left element - the size of the right element.
        #     Zero out the space of the left element.
        #     Prepend disk2 with all the elements again, completing the insert operation
        #     the final element of disk2 should have the space of the left element added to it (size+empty).
        #     Decrease the max_id allowed, so that we do not accidentally compactify the same item again
        # If we come to the end of the list without triggering this, then 
        while max_id > 0:
            x = disk2.pop()
            r_id, r_size, r_space = x
            if r_id > max_id:
                the_tail.appendleft(x)
                continue
            
            the_front = deque()
            while True:
                try:
                    y = disk2.popleft()
                # If we walked through the whole disk2 without finding a place for x
                except IndexError:
                    the_front.extend(disk2)
                    disk2 = the_front
                    the_tail.appendleft(x)
                    max_id-=1
                    break
                l_id, l_size, l_space = y
                if l_space >= r_size:
                    disk2.appendleft((r_id,r_size,l_space-r_size))
                    disk2.appendleft((l_id,l_size,0))
                    z = disk2.pop()
                    z_id, z_size, z_space = z
                    disk2.append((z_id, z_size, z_space+r_space+r_size))
                    the_front.extend(disk2)
                    disk2 = the_front
                    max_id-=1
                    break
                else:
                    the_front.append(y)
            
        disk2.extend(the_tail)
        f = lambda i,s,x_id,x_size,x_space: (i+x_size+x_space,s+x_id*(x_size*(2*i+x_size-1)//2))
        _, checksum = reduce(lambda a,x: f(*a,*x), disk2, (0,0))
        print(checksum)

                    
            
            
        
        

if __name__ == "__main__":
    main()
