import re

def main():
    filename = "day3_input"
    with open(filename, 'r') as the_file:
        the_text = the_file.read()
        print(the_text)
        pairs = re.findall("mul\((\d+),(\d+)\)", the_text)
        answer1 = sum(map(lambda x: int(x[0])*int(x[1]), pairs))
        print(answer1)
        tokens = re.finditer("(?P<mul>mul\((\d+),(\d+)\))|(?P<do>do\(\))|(?P<dont>don't\(\))",
                             the_text)

        answer2 = 0
        allow_mul = True
        for toke in tokens:
            kind = toke.lastgroup
            
            if kind == "do":
                allow_mul = True
            elif kind == "dont":
                allow_mul = False
            else:
                (x,y) = toke.group(2,3)
                answer2 += int(x)*int(y) if allow_mul else 0

        print(answer2)
                      
if __name__ == "__main__":
    main()
