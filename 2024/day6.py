def simulate(room, starting_position, starting_velocity):
    (x,y) = starting_position
    height = len(room)
    width = len(room[0])
    (vx, vy) = starting_velocity
    in_bounds = lambda i,j: i>=0 and i<width and j>=0 and j<height
    v_to_compass = {(-1,0):'W', (1,0):'E', (0,1):'N', (0,-1):'S'}
    compass_to_v = dict((y,x) for (x,y) in v_to_compass.items())
    while True:
        # first check if the next step is in bounds
        if not in_bounds(x+vx,y+vy):
            break
        
        # If there is something directly in front of you, turn right 90 degrees.
        # Otherwise, take a step forward.
        next_space = room[-1-(y+vy)][x+vx]
        if next_space == '#':
            # rotate clockwise (rotation matrix with -pi/2)
            (vx,vy) = (vy,-vx)
        else:
            # Check here if we are about to enter a loop
            if v_to_compass[vx,vy] == next_space:
                return True
            x+=vx
            y+=vy
            room[-y-1][x]=v_to_compass[vx,vy]
    return False

def simulate_obstacles(original_room, obstacles, starting_position, starting_velocity):
    clone_room = lambda : [line[:] for line in original_room]
    def test_obstacle(i,j):
        cloned_room = clone_room()
        cloned_room[i][j] = '#'
        return simulate(cloned_room, starting_position, starting_velocity)
    return sum(1 for obstacle in obstacles if test_obstacle(*obstacle))        
    
def main():
    filename = "day_6_input"
    with open(filename, 'r') as the_file:
        room = [list(line.strip()) for line in the_file.readlines()]
        original_room = [line[:] for line in room]
        height = len(room)
        for (i,line) in enumerate(room):
            try:
                j = line.index('^')
                starting_position = (j, height-1-i)
                break
            except ValueError:
                continue
            
        (x,y) = starting_position
        room[-y-1][x] = 'N'
        starting_velocity = (0,1)
        count = simulate(room, starting_position, starting_velocity)
        obstacles = [(i,j) for (i, line) in enumerate(room) for (j,x) in enumerate(line) if x in 'NESW' ]
        print(len(obstacles))
        print(simulate_obstacles(original_room, obstacles, starting_position, starting_velocity))

if __name__ == "__main__":
    main()
