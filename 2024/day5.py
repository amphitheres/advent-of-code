def bubble_sort_mid(xs, order):
    for i in range(len(xs)):
        for j in range(i, len(xs)):
            if (xs[j],xs[i]) in order:
                tmp = xs[i]
                xs[i] = xs[j]
                xs[j] = tmp
    return xs[len(xs)//2]

def main():
    filename = "day_5_test"
    with open(filename, 'r') as the_file:
        raw_data = list(map(lambda x: x.strip(), the_file.readlines()))
        separator = raw_data.index("")

        raw_page_orders = raw_data[:separator]
        raw_updates = raw_data[separator+1:]
        
        page_orders = set(tuple(map(int, x.split('|'))) for x in raw_page_orders)
        updates = [[int(y) for y in x.split(',')] for x in raw_updates]

        is_valid = lambda x: not any((x[j], x[i]) in page_orders for i in range(len(x)) for j in range(i+1,len(x)))
        answer1 = sum(int(x[len(x)//2]) for x in updates if is_valid(x))
        print(answer1)
        invalid_updates = filter(lambda x: not is_valid(x), updates)
        answer2 = sum(bubble_sort_mid(xs, page_orders) for xs in invalid_updates)
        print(answer2)

        

        
            
        

if __name__ == "__main__":
    main()
