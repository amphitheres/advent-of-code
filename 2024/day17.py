import re
from enum import IntEnum
from collections import namedtuple

class Operation(IntEnum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7
Processor = namedtuple('Processor', ['ra','rb','rc','ip','program'])

def literal(p):
    return p.program[p.ip+1]
def combo(p):
    x = p.program[p.ip+1]
    if 0<=x<=3:
        return x
    elif x == 4:
        return p.ra
    elif x == 5:
        return p.rb
    elif x == 6:
        return p.rc
    assert False, "Invalid operand {x}."
def process(p):
    op = Operation(p.program[p.ip])
    if op is Operation.ADV:
        return None, p._replace(ra=p.ra>>combo(p),ip=p.ip+2)
    elif op is Operation.BXL:
        return None, p._replace(rb=p.rb^literal(p),ip=p.ip+2)
    elif op is Operation.BST:
        return None, p._replace(rb=combo(p) % 8,ip=p.ip+2)
    elif op is Operation.JNZ:
        if bool(p.ra):
            return None,p._replace(ip=literal(p))
        return None,p._replace(ip=p.ip+2)
    elif op is Operation.BXC:
        return None,p._replace(rb=p.rb^p.rc,ip=p.ip+2)
    elif op is Operation.OUT:
        return str(combo(p) % 8),p._replace(ip=p.ip+2)
    elif op is Operation.BDV:
        return None,p._replace(rb=p.ra>>combo(p),ip=p.ip+2)
    elif op is Operation.CDV:
        return None,p._replace(rc=p.ra>>combo(p),ip=p.ip+2)
    assert False, "Did not process an operation for some reason."
    
def part1(ra,rb,rc, program):
    # instruction pointer
    p = Processor(ra,rb,rc,0,program)
    is_valid = lambda p:0<=p.ip<len(p.program)
    output = []
    while is_valid(p):
        x,p = process(p)
        if x:
            output.append(x)
    print(','.join([str(x) for x in output]))
    return tuple(int(x) for x in output)


def str_combo(y):
    if 0 <= y <= 3:
        return str(y)
    elif 4 <= y <= 6:
        return 'r'+("abc"[y-4])
    assert False, "Invalid combo operand."
        
def str_instruction(op,y):
    s = f"{op.name},{y}:"
    if op is Operation.ADV:
        return s+f"ra=ra>>{str_combo(y)}"
    elif op is Operation.BXL:
        return s+f"rb=rb^{y}"
    elif op is Operation.BST:
        return s+f"rb={str_combo(y)} % 8"
    elif op is Operation.JNZ:
        return s+f"goto {y} if ra!=0"
    elif op is Operation.BXC:
        return s+f"rb=rb^rc"
    elif op is Operation.OUT:
        return s+f"output {str_combo(y)} % 8"
    elif op is Operation.BDV:
        return s+f"rb=p.ra>>{str_combo(y)}"
    elif op is Operation.CDV:
        return s+f"rc=ra>>{str_combo(y)}"
        

def part2(ra,rb,rc,program):
    # ip = 0
    # instructions = program
    # pretty print out instructions for program analysis by hand
    # while instructions:
    #     x,y,*instructions = instructions
    #     print(str(ip)+"::"+str_instruction(Operation(x), y))
    #     ip+=1

    # worked out on paper a test. Idea is to see if the program will
    # output y given x
    test = lambda x, y: (lambda z: (y ^ 5 ^ (x>>(z^1)))%8 == z)(x % 8)
    xs = [0]
    # based on the program analysis, the way the program works
    # it prints out an octal digit based on octal digits of x
    # we know the octal digits of x end in 0 and so we can work backwards
    # from there using a little trial and error.
    # Each step introduces multiple possibilities which we prune.
    for y in program[::-1]:
        xss = []
        for x in xs:
            xss.extend([(x<<3)+i for i in range(8) if test((x<<3)+i,y)])
        xs = xss
    result = min(xs)
    print(result)
    return result
        
    
def main():
    fname = "day_17_input"
    with open(fname, 'r') as f:
        digits = re.compile('\d+')
        data = f.readlines()
        ra,rb,rc = *(int(digits.search(data[i])[0]) for i in range(3)),
        program = tuple(int(x) for x in digits.findall(data[4]))

        output = part1(ra,rb,rc,program)
        part2(ra,rb,rc,program)
        
if __name__ == "__main__":
    main()
