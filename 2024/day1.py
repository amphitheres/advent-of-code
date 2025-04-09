import sys
from collections import Counter


def main():
    filename = "day1_problem1_input"
    the_file = open(filename, "r")
    
    get_pair = lambda line: map(int, line.split())
    [list1,list2] = map(sorted,
                zip(*map(get_pair,
                         the_file.readlines())))
    answer1 = sum(map(lambda x: abs(x[0]-x[1]), zip(list1,list2)))
    
    print(answer1)
    similarity_score = Counter(list2)
    answer2 = sum(map(lambda x: x*similarity_score[x], list1))
    print(answer2)
        
if __name__ == "__main__":
    main()
