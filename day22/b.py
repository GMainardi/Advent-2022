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

    def move_between_rooms(self, step: tuple[int], maze: 'Maze'):
        curr_room = maze.get_curr_room(self.pos)
        match curr_room:
            case 'A':
                match self.looking:
                    case (0, -1):
                        step = (step[0]-100, 199)
                        facing = (0, -1)
                        return step, facing
                    case (1, 0):
                        step = (99, 149-step[1])
                        facing = (-1, 0)
                        return step, facing
                    case (0, 1):
                        step = (99, step[0]-50)
                        facing = (-1, 0)
                        return step, facing
                    case (-1, 0):
                        return step, self.looking
            case 'B':
                match self.looking:
                    case (0, -1):
                        step = (0, step[0]+100)
                        facing = (1, 0)
                        return step, facing
                    case (1, 0):
                        return step, self.looking
                    case (0, 1):
                        return step, self.looking
                    case (-1, 0):
                        step = (0, 149-step[1])
                        facing = (1, 0)
                        return step, facing
            case 'C':
                match self.looking:
                    case (0, -1):
                        return step, self.looking
                    case (1, 0):
                        step = (step[1]+50, 49)
                        facing = (0, -1)
                        return step, facing
                    case (0, 1):
                        return step, self.looking
                    case (-1, 0):
                        step = (step[1]-50, 100)
                        facing = (0, 1)
                        return step, facing
            case 'D':
                match self.looking:
                    case (0, -1):
                        return step, self.looking
                    case (1, 0):
                        step = (149, 149-step[1])
                        facing = (-1, 0)
                        return step, facing
                    case (0, 1):
                        step = (49, step[0]+100)
                        facing = (-1, 0)
                        return step, facing
                    case (-1, 0):
                        return step, self.looking
            case 'E':
                match self.looking:
                    case (0, -1):
                        return step, self.looking
                    case (1, 0):
                        step = (step[1]-100, 149)
                        facing = (0, -1)
                        return step, facing
                    case (0, 1):
                        step = (step[0]+100, 0)
                        facing = (0, 1)
                        return step, facing
                    case (-1, 0):
                        step = (step[1]-100, 0)
                        facing = (0, 1)
                        return step, facing
            case 'F':
                match self.looking:
                    case (0, -1):
                        step = (50, step[0]+50)
                        facing = (1, 0)
                        return step, facing
                    case (1, 0):
                        return step, self.looking
                    case (0, 1):
                        return step, self.looking
                    case (-1, 0):
                        step = (50, 149-step[1])
                        facing = (1, 0)
                        return step, facing

    def walk(self, steps: int, maze: 'Maze'):
        for _ in range(steps):

            step = self.__next_step()
            curr_room = maze.get_curr_room(self.pos)
            step_room = maze.get_curr_room(step)
            facing = self.looking

            if curr_room != step_room:
                print(f'{curr_room=}')
                # print(f'{self.pos=}')
                # print(f'{step=}')
                # print(f'{self.looking=}')
                step, facing = self.move_between_rooms(step, maze)
                print(f'{step=}')
                print()

            if any([step in room.walls for room in maze.rooms]):
                break
            

            self.pos = step
            self.looking = facing

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

    def get_curr_room(self, pos:tuple[int]):
        if 100 <= pos[0] <= 149 \
        and 0 <= pos[1] <= 49:
            return 'A'
        if 50 <= pos[0] <= 99 \
        and 0 <= pos[1] <= 49:
            return 'B'
        if 50 <= pos[0] <= 99 \
        and 50 <= pos[1] <= 99:
            return 'C'
        if 50 <= pos[0] <= 99 \
        and 100 <= pos[1] <= 149:
            return 'D'
        if 0 <= pos[0] <= 49 \
        and 150 <= pos[1] <= 199:
            return 'E'
        if 0 <= pos[0] <= 49 \
        and 100 <= pos[1] <= 149:
            return 'F'

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

print(me.pos)

final_password = (1000*(me.pos[1]+1)) + \
                 (4*(me.pos[0]+1)) + \
                  facing

print(final_password)