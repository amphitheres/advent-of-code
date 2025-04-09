def main():
    filename = "day_4_input"
    with open(filename, 'r') as the_file:
        grid = list(line.strip() for line in the_file.readlines())
        width = len(grid[0])
        
        height = len(grid)
        print(repr(grid[0]))
        print("width", width, "height", height)
        in_grid = lambda x,y: x>=0 and x<width and y>=0 and y<height
        trajectories = [(i,j) for i in [-1,0,1] for j in [-1,0,1] if (i!=0 or j!=0)]
        lxmas = len("XMAS")
        paths = lambda x, y: (((x+i*vx,y+i*vy) for i in range(lxmas))
                              for (vx,vy) in trajectories if in_grid(x+(lxmas-1)*vx,y+(lxmas-1)*vy))
        substrs = ["".join(grid[i][j] for (i,j) in path) for x in range(width) for y in range(height) for path in paths(x,y)]
        answer1 = sum(map(lambda x: "XMAS" == x, substrs))
        print(answer1)

        lmas = len("MAS")
        is_mas = lambda x: x == "MAS" or x == "SAM"
        answer2 = 0
        for x in range(width):
            for y in range(height):
                try:
                    forwardslash = "".join(grid[x-1+i][y-1+i] for i in range(lmas))
                    backslash = "".join(grid[x-1+i][y+1-i] for i in range(lmas))
                    if is_mas(forwardslash) and is_mas(backslash):
                        answer2+=1
                except IndexError:
                    pass
        print(answer2)
                

if __name__ == "__main__":
    main()
