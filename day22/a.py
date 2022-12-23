import re

class Me:

    def __init__(self, pos) -> None:
        self.pos = pos
        self.looking = (1, 0)
        self.room = 0

    def rotation(self, direction: str) -> None:
        match direction:
            case 'R':
                self.__rotate_clockwise()
            case 'L':
                self.__rotate_anticlockwise()

    def __rotate_clockwise(self) -> None:
        self.looking = (-self.looking[1], self.looking[0])

    def __rotate_anticlockwise(self) -> None:
        self.looking = (self.looking[1], -self.looking[0])

    def command(self, command, maze: 'Maze'):
        if type(command) == int:
            self.walk(command, maze)
        else:
            for c in command:
                self.rotation(c)
    
    def get_next_room_step(self, step: tuple[int], maze: 'Maze'):
        next_room_idx = (self.room+1) % len(maze.rooms)
        next_room = maze.rooms[next_room_idx]
        if step[0] >= next_room.start[0] and step[0] <= next_room.end[0]:
            return (step[0], next_room.start[1])
        else:
            for room in maze.rooms:
                if step[0] >= room.start[0] and step[0] <= room.end[0]:
                    return (step[0], room.start[1])
    
    def get_prev_room_step(self, step: tuple[int], maze: 'Maze'):
        prev_room_idx = (self.room-1) % len(maze.rooms)
        prev_room = maze.rooms[prev_room_idx]
        if step[0] >= prev_room.start[0] and step[0] <= prev_room.end[0]:
            return (step[0], prev_room.end[1])
        else:
            for room in maze.rooms[::-1]:
                if step[0] >= room.start[0] and step[0] <= room.end[0]:
                    return (step[0], room.end[1])

    def get_curr_room(self, maze):
        for idx, room in enumerate(maze.rooms):
            if room.start[0] <= self.pos[0] <= room.end[0] \
            and room.start[1] <= self.pos[1] <= room.end[1]:
                return idx
        
    def walk(self, steps: int, maze: 'Maze'):
        for _ in range(steps):

            curr_room = maze.rooms[self.room]
            step = self.__next_step()
            if step[0] > curr_room.end[0]:
                step = (curr_room.start[0], step[1])
            elif step[0] < curr_room.start[0]:
                step = (curr_room.end[0], step[1])
            elif step[1] > curr_room.end[1]:
                step = self.get_next_room_step(step, maze)
            elif step[1] < curr_room.start[1]:
                step = self.get_prev_room_step(step, maze)
            if any([step in room.walls for room in maze.rooms]):
                break

            self.pos = step
            self.room = self.get_curr_room(maze)

    def __next_step(self):
        return (self.pos[0]+self.looking[0],
                self.pos[1]+self.looking[1])

class Room:

    def __init__(self, start: tuple[int], end: tuple[int], walls: set[tuple[int]]) -> None:
        self.start = start
        self.end = end
        self.walls = walls

    @classmethod
    def from_str_desc(cls, desc: list[str], prev_end: int) -> 'Room':
        start = (min(desc[0].index('.'), desc[0].index('#')), prev_end)
        end = (len(desc[0])-1, len(desc)-1 + prev_end)

        walls = set([])
        for row, line in enumerate(desc):
            for col, symb in enumerate(line):
                if symb == '#':
                    walls.add((col, row+start[1]))

        return Room(start, end, walls)

    def __repr__(self) -> str:
        ans = ''
        ans += f'{self.start=}\t{self.end=}\n'
        for y in range(self.start[1], self.end[1]+1):
            ans += ' ' * self.start[0]
            for x in range(self.start[0], self.end[0]+1):
                if (x, y) in self.walls:
                    ans += '#'
                else:
                    ans += '.'
            ans += '\n'
        return ans

class Maze:

    def __init__(self) -> None:
        self.rooms = []
    
    def add_room(self, room_desc: list[str], prev_end: int = 0) -> None:
        self.rooms.append(Room.from_str_desc(room_desc, prev_end))

    def __repr__(self) -> str:
        ans = ''
        for room in self.rooms:
            ans += str(room)
        return ans
    
def split_room(input: list[str]) -> list[str]:
    desc = [input[0]]
    min_x = min(desc[0].index('.'), desc[0].index('#'))
    end = len(desc[0])-1
    line = 1
    while end == len(input[line])-1 and (min_x == 0 or input[line][min_x-1] == ' '):
        desc.append(input[line])
        line += 1
    return desc


maze = Maze()

with open('input.txt', 'r') as file:
    input = [line[:-1] for line in file.readlines()]
    curr_start_room = 0
    while curr_start_room != len(input)-2:
        room = split_room(input[curr_start_room:-1])
        maze.add_room(room, curr_start_room)
        curr_start_room += len(room)
    path = [int(p) if p.isnumeric() else p for p in re.split('(\d+)', input[-1])]

#print(maze)

me = Me(maze.rooms[0].start)
for command in path:
    me.command(command, maze)

facing = 0
match me.looking:
    case (1, 0):
        facing = 0
    case (0, 1):
        facing = 1
    case (-1, 0):
        facing = 2
    case (0, -1):
        facing = 3

final_password = (1000*(me.pos[1]+1)) + \
                 (4*(me.pos[0]+1)) + \
                  facing
print(final_password)