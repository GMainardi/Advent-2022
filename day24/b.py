from dataclasses import dataclass
from enum import Enum, auto


@dataclass(frozen=True)
class Me:
    x: int = 1
    y: int = 0

    @property
    def adj_moves(self):
        stay = (self.x, self.y)
        up = (self.x, self.y-1)
        down = (self.x, self.y+1)
        left = (self.x-1, self.y)
        right = (self.x+1, self.y)
        return [stay, up, down, left, right]

    def check_occuped_space(self, storm: tuple, move: tuple[int]):
        for b in storm:
            if move in b:
                return True
        return False

    def moves(self, storm: tuple):
        global x_lim
        global y_lim
        possible_moves = []
        for move in self.adj_moves:
            if self.check_occuped_space(storm, move):
                continue
            elif move[0] == x_lim-1 and move[1] == y_lim:
                possible_moves.append(move)
            elif move[0] == 1 and move[1] == 0:
                possible_moves.append(move)
            elif move[0] <= 0 or move[1] <= 0:
                continue
            elif move[0] == x_lim or move[1] == y_lim:
                continue
            else:
                possible_moves.append(move)
        return possible_moves

def update_up(blizzards: set[tuple]):
    global y_lim
    new_up = set([])
    for x, y in blizzards:
        y -= 1
        if y == 0:
            y = y_lim -1
        new_up.add((x,y))
    return new_up

def update_down(blizzards: set[tuple]):
    global y_lim
    new_down = set([])
    for x, y in blizzards:
        y += 1
        if y == y_lim:
            y = 1
        new_down.add((x,y))
    return new_down

def update_left(blizzards: set[tuple]):
    global x_lim
    new_left = set([])
    for x, y in blizzards:
        x -= 1
        if x == 0:
            x = x_lim -1
        new_left.add((x,y))
    return new_left

def update_right(blizzards: set[tuple]):
    global x_lim
    new_right = set([])
    for x, y in blizzards:
        x += 1
        if x == x_lim:
            x = 1
        new_right.add((x,y))
    return new_right

def all_storms(storm: tuple):
    global x_lim
    global y_lim
    states = []
    while storm not in states:
        states.append(storm)
        up_b = update_up(storm[0])
        down_b = update_down(storm[1])
        left_b = update_left(storm[2])
        right_b = update_right(storm[3])
        storm = (up_b, down_b, left_b, right_b)
    return states
    
def get_min_path(states: list, start: tuple, end: tuple, storm_id: int = 0):
    storm_id %= len(states)
    me = Me(start[0], start[1])
    node = (me, storm_id)
    visited = set([node])
    queue = [node]
    dists = {node: 0}
    while queue:
        pos, storm_id = queue.pop(0)
        if pos.x == end[0] and pos.y == end[1]:
            return dists[(pos, storm_id)]
        next_storm = (storm_id + 1) % len(states)
        for step in pos.moves(states[next_storm]):
            neig = (Me(step[0], step[1]), next_storm)
            if neig not in visited:
                visited.add(neig)
                queue.append(neig)
                dists[neig] = dists[(pos, storm_id)] + 1

input = [line.strip() for line in open('input.txt')]

x_lim = len(input[0])-1
y_lim = len(input)-1

storm = (set([]), set([]), set([]), set([]))
for y, line in enumerate(input):
    for x, char in enumerate(line):
        match char:
            case '^':
                storm[0].add((x, y))
            case 'v':
                storm[1].add((x, y))
            case '<':
                storm[2].add((x, y))
            case '>':
                storm[3].add((x, y))

storms = all_storms(storm)
start = (1, 0)
end = (x_lim-1, y_lim)
first = get_min_path(storms, start, end, 0)
second = get_min_path(storms, end, start, first)
third = get_min_path(storms, start, end, first+second)
print(first+second+third)