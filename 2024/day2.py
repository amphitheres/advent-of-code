from itertools import chain

def main():
    filename = "day2_test1"
    the_file = open(filename, "r")

    reports = list(map(lambda xs: list(map(int, xs.split())), the_file.readlines()))
    
    def test_levels(report):
        diffs = list(map(lambda x: x[1]-x[0], zip(report[:-1],report[1:])))
        test1 = all(map(lambda x: x>0, diffs)) or all(map(lambda x: x<0,diffs))
        test2 = max(map(abs, diffs)) <= 3
        return test1 and test2
    
    tested_reports = map(test_levels, reports)
    answer1 = sum(tested_reports)
    print(answer1)
    reports_with_dampened = map(lambda xs: chain([xs],
                                                 (xs[:i]+xs[i+1:] for i in range(len(xs)))),
                                reports)
    tested_rep_w_damp = map(lambda xss: any(map(test_levels, xss)), reports_with_dampened)
    answer2 = sum(tested_rep_w_damp)
    print(answer2)

if __name__== "__main__":
    main()
