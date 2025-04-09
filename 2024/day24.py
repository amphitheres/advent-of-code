import re
from enum import Enum, auto
from itertools import starmap, chain
from functools import reduce
from operator import and_, or_, xor
fset = frozenset    
Op = {'AND':and_,
      'OR':or_,
      'XOR':xor}
def split_data(data):
    for i,x in enumerate(data):
        if not x:
            return data[:i],*split_data(data[i+1:])
    return (data,)
            
def parse_input(fname):
    with open(fname, 'r') as f:
        
        data = tuple(l.strip() for l in f.read().strip().split('\n'))
        wire_data, instruction_data = split_data(data)

        wire = re.compile('(\w+): (\d+)')
        parse_wire = lambda x:(lambda a,b:(a,int(b)))(*(wire.match(x).groups()),)
        
        wires = tuple(parse_wire(x.strip()) for x in wire_data)

        instruction = re.compile('(\w+) (\w+) (\w+) -> (\w+)')
        parse_instruction = lambda x: (*(instruction.match(x).groups()),)
        instructions = tuple(parse_instruction(x) for x in instruction_data)
        
        return wires, instructions


def eval_wire(D,W,w):
    try:
        return W[w]
    except KeyError: pass
    a,b,c = D[w]
    W[w] = Op[b](eval_wire(D,W,a), eval_wire(D,W,c))
    return W[w]

        

def part1(wires, instructions):

    W = dict(wires)
    saved = {w:0 for w,_ in wires}
    D = dict()
    for a,b,c,d in instructions:
        if d in D:
            print(d)
        D[d] = (a,b,c)
    zs = [d for _,_,_,d in instructions if d[0]=='z']
    zs.sort()
    print(reduce((lambda x,y:(x<<1)|eval_wire(D,W,y)),zs[::-1],0))

def correct_z_error(op_to_alias,z):
    for i in range(46):
        try:
            if op_to_alias[z(i)] != f"z{i:02}":
                k = next(x for x,y in op_to_alias.items() if y == f"z{i:02}")
                op_to_alias[z(i)], op_to_alias[k] = f"z{i:02}",op_to_alias[z(i)]
                return f"z{i:02}",op_to_alias[k]
        except KeyError:
            # in this second case, we assume that op_to_alias already has the
            # correct operation pointing to z_i. If z(i) and correct_op differ
            # by only 2 aliases, we can swap them 
            correct_op = next(x for x,y in op_to_alias.items() if y == f"z{i:02}")
            swap_set = (z(i) ^ correct_op) - fset(['AND','OR','XOR'])
            if len(swap_set) == 2:
                alias1, alias2 = *swap_set,
                k1 = next(x for x,y in op_to_alias.items() if y == alias1)
                k2 = next(x for x,y in op_to_alias.items() if y == alias2)
                op_to_alias[k1], op_to_alias[k2] = alias2, alias1
                return alias1,alias2

def part2(wires, instructions):
    bin_to_int = lambda xs: reduce(lambda x,y: (x<<1)|y[1],xs,0)
    
    xs = [(x,y) for x,y in wires if x[0]=='x']
    x = bin_to_int(sorted(xs,reverse=True))
    ys = [(x,y) for x,y in wires if x[0]=='y']
    y = bin_to_int(sorted(ys,reverse=True))

    op_to_alias = {fset([a,b,c]):d for a,b,c,d in instructions}
    
    
    a = lambda i: fset([f"x{i:02}",f"y{i:02}","XOR"])
    d = lambda i: fset([f"x{i:02}",f"y{i:02}","AND"])
    e = lambda i: fset([op_to_alias[c(i)],op_to_alias[a(i)],'AND'])
    c = lambda i: d(0) if i == 1 else fset([op_to_alias[d(i-1)],op_to_alias[e(i-1)],'OR'])
    z = lambda i: a(0) if i == 0 else c(45) if i == 45 else fset([op_to_alias[a(i)],op_to_alias[c(i)],'XOR'])
    errors = []
    err = correct_z_error(op_to_alias,z)
    if err:
        errors.append(err)
    err = correct_z_error(op_to_alias, z)
    if err:
        errors.append(err)
    err = correct_z_error(op_to_alias, z)
    if err:
        errors.append(err)
    err = correct_z_error(op_to_alias, z)
    if err:
        errors.append(err)
    for i in range(0,46):
        if i in range(0,45):
            try:
                print(f"a{i:02}:",a(i))
                print("alias:",op_to_alias[a(i)])
            except:
                print("a failed")
            try:
                print(f"d{i:02}:",d(i))
                print("alias:",op_to_alias[d(i)])
            except:
                print("d failed")
            
        if i in range(1,46):
            try:
                print(f"c{i:02}:",c(i))
                print("alias:",op_to_alias[c(i)])
            except:
                print("c failed")
        if i in range(1,45):
            try:
                print(f"e{i:02}:",e(i))
                print("alias:",op_to_alias[e(i)])
            except:
                print("e failed")
        try:
            print(f"z{i:02}:",z(i))
            print("alias:",op_to_alias[z(i)])
        except:
            print("z failed")
        print()
    errors = sorted(chain.from_iterable(errors))
    print(','.join(errors))
    

    
def main():
    fname = "day24_input"
    wires, instructions = parse_input(fname)
    part1(wires, instructions)
    part2(wires, instructions)

if __name__ == "__main__":
    main()
    
