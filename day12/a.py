def get_starter_node(map):
    for x, row in enumerate(map):
        for y, letter in enumerate(row):
            if letter == 'S':
                return (x, y)

def get_possible_steps(map, pos):
    left = (pos[0], pos[1]-1) if pos[1]-1 >= 0 else None
    right = (pos[0], pos[1]+1) if pos[1]+1 < len(map[0]) else None
    up = (pos[0]-1, pos[1]) if pos[0]-1 >= 0 else None
    down = (pos[0]+1, pos[1]) if pos[0]+1 < len(map) else None

    steps = [up, down, left, right]
    neighbors = []
    for step in steps:
        if step is None:
            continue

        if map[step[0]][step[1]] == 'E':
            if ord(map[pos[0]][pos[1]]) >= ord('z')-1:
                neighbors.append(step)

        elif map[pos[0]][pos[1]] == 'S':
                neighbors.append(step)

        elif ord(map[pos[0]][pos[1]]) >= ord(map[step[0]][step[1]])-1:
            neighbors.append(step)
    return neighbors


def BFS(map, start):
    queue = []

    visited = {(x, y): False for x in range(len(map)) for y in range(len(map[x]))}

    dist = {(x, y): float('inf') for x in range(len(map)) for y in range(len(map[x]))}

    visited[start] = True
    dist[start] = True
    queue.append(start)

    while len(queue):
        curr = queue.pop(0)
        adjs = get_possible_steps(map, curr)
        for neibhbor in adjs:
            if not visited[neibhbor]:
                visited[neibhbor] = True
                dist[neibhbor] = dist[curr] + 1
                queue.append(neibhbor)

                if map[neibhbor[0]][neibhbor[1]] == 'E':
                    return dist[neibhbor] -1

map = [[letter for letter in line.strip()] for line in open('input.txt')]


print(f'starter node: {get_starter_node(map)}')
print(f'shortest path lenght: {BFS(map, get_starter_node(map))}')
