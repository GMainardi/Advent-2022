def move(T, dir):
    match dir:
        case 'U':
            return (T[0], T[1]+1)
        case 'R':
            return (T[0]+1, T[1])
        case 'D':
            return (T[0], T[1]-1)
        case 'L':
            return (T[0]-1, T[1])

def dist(T, H):
    direction = (H[0]-T[0], H[1]-T[1])

    if abs(direction[0]) <= 1 and abs(direction[1]) <= 1:
        return (0,0)
    elif direction[0] == 0:
        return (0, direction[1]//abs(direction[1]))
    elif direction[1] == 0:
        return (direction[0]//abs(direction[0]), 0)
    elif direction[0] > 0 and direction[1] > 0:
        return (1, 1)
    elif direction[0] > 0 and direction[1] < 0:
        return (1, -1)
    elif direction[0] < 0 and direction[1] > 0:
        return (-1, 1)
    elif direction[0] < 0 and direction[1] < 0:
        return (-1, -1)

def update_T(T, v):
    return (T[0]+v[0], T[1]+v[1])


def show_step(H, T):
    top = (max(H[0], T[0])+1, max(H[1], T[1])+1)
    for y in range(top[1], -1, -1):
        for x in range(0, top[0]+1):
            if (x, y) == H:
                print('H', end='')
            elif (x, y) == T:
                print('T', end='')
            else:
                print('.', end='')
        print()

def show_visited(visited):
    top = (max(list(map(lambda x : x[0], visited)))+1, max(list(map(lambda x : x[1], visited)))+1)
    for y in range(top[1], -1, -1):
        for x in range(0, top[0]+1):
            if (x, y) in visited:
                print('#', end='')
            else:
                print('.', end='')
        print()  
input = [(line.strip().split()[0], int(line.strip().split()[1])) for line in open('input.txt')]

H = (0, 0)
T = (0, 0)
T_visit = set([T])

for command in input:
    dir, steps = command
    for _ in range(steps):
        H = move(H, dir)
        dist_vector = dist(T, H)
        T = update_T(T, dist_vector)
        T_visit.add(T)

show_visited(T_visit)

print(len(T_visit))