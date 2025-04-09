import re
import itertools

def main():
    filename = "day_7_input"
    with open(filename, 'r') as the_file:
        p = re.compile('\W+')
        operations = [[int(x) for x in p.split(line.strip())] for line in the_file.readlines()]

        def is_operation_result(result, x, *xs):
            combos = itertools.product(*tuple(('*','+') for i in range(len(xs))))
            for combo in combos:
                ys = zip(combo,xs)
                accumulate = x
                for (op, y) in ys:
                    if op == '*':
                        accumulate*=y
                    elif op == '+':
                        accumulate+=y
                if accumulate == result:
                    return result
            return 0
        def is_operation_result_with_concat(result, x, *xs):
            combos = itertools.product(*tuple(('*','+', '|') for i in range(len(xs))))
            for combo in combos:
                ys = zip(combo,xs)
                accumulate = x
                for (op, y) in ys:
                    if op == '*':
                        accumulate*=y
                    elif op == '+':
                        accumulate+=y
                    elif op == '|':
                        accumulate = int(str(accumulate)+str(y))
                if accumulate == result:
                    return result
            return 0
        print(sum(is_operation_result(*x) for x in operations))
        print(sum(is_operation_result_with_concat(*x) for x in operations))
if __name__ == "__main__":
    main()
