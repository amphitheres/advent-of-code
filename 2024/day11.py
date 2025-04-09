from collections import deque

# takes a deque of ints, processes n of them
# returns the number of new stones
def blink(stones, n):
    m = 0
    for _ in range(n):
        stone = stones.pop()
        s = str(stone)
        len_s = len(s)
        if stone == 0:
            stones.appendleft(1)
            m+=1
        elif not(len_s & 1):
            stones.appendleft(int(s[len_s>>1:]))
            stones.appendleft(int(s[:len_s>>1]))
            m+=2
        else:
            stones.appendleft(stone*2024)
            m+=1
    return m
            
def stone_value(stone, n, scores):
    # base case
    if n <= 0:
        return 1
    try:
        return scores[stone, n]
    except KeyError:
        pass
    if stone == 0:
        # always memoize this case
        scores[stone,n] = stone_value(1,n-1,scores)
        return scores[stone,n]
    s = str(stone)
    len_s = len(s)
    if len_s & 1:
        val = stone_value(stone*2024, n-1, scores)
    else:
        mid = len_s>>1
        val = (stone_value(int(s[:mid]),n-1,scores)
               + stone_value(int(s[mid:]),n-1,scores))
    # memoize for some 'small' number stones
    if len_s < 5:
        scores[stone,n] = val
        
    return val

def part1(data):
    stones = deque(data)
    n = len(stones)
    k = 25
    for _ in range(k):
        n = blink(stones, n)
    print(n)

def part2(data):
    # we will try a recursive approach with partial memoization
    # should be much faster as long as we memoize in a particular order
    scores = dict()
    k = 75
    # intuitively it would seem better to memoize small values of n first
    # then build up to higher values.
    for n in range(k//2):
        for stone in range(10**5):
            stone_value(stone,n,scores)
    print(sum((stone_value(stone, k, scores) for stone in data)))
    

def main():
    filename = "day_11_input"
    with open(filename, 'r') as the_file:
        data = tuple((int(x) for x in the_file.read().strip().split()))
        print(data)
        part1(data)
        part2(data)


if __name__ == "__main__":
    main()
