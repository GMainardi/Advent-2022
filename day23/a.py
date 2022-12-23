from dataclasses import dataclass, field
from enum import Enum, auto

class Direction(Enum):
    North = auto()
    South = auto()
    East = auto()
    West = auto()
    NorthEast = auto()
    NorthWest = auto()
    SouthEast = auto()
    SouthWest = auto()

@dataclass(frozen=True)
class Elf:
    x: int
    y: int
    priority: tuple['Direction'] = (Direction.North, Direction.South, Direction.West, Direction.East)

    @property
    def North(self) -> tuple[int]:
        return (self.x  , self.y-1)

    @property
    def South(self) -> tuple[int]:
        return (self.x  , self.y+1)
    
    @property
    def East(self) -> tuple[int]:
        return (self.x+1, self.y  )

    @property
    def West(self) -> tuple[int]:
        return (self.x-1, self.y  )

    @property
    def NorthEast(self) -> tuple[int]:
        return (self.x+1, self.y-1)

    @property
    def NorthWest(self) -> tuple[int]:
        return (self.x-1, self.y-1)

    @property
    def SouthEast(self) -> tuple[int]:
        return (self.x+1, self.y+1)
    
    @property
    def SouthWest(self) -> tuple[int]:
        return (self.x-1, self.y+1)

    @property
    def adj_coords(self) -> list[tuple[int]]:
        return [self.North, self.South,
                self.East, self.West,
                self.NorthEast, self.NorthWest,
                self.SouthEast, self.SouthWest]
    
    @property
    def req_move_north(self) -> list[tuple[int]]:
        return [self.North,
                self.NorthEast,
                self.NorthWest]
    
    @property
    def req_move_south(self) -> list[tuple[int]]:
        return [self.South,
                self.SouthEast,
                self.SouthWest]
    
    @property
    def req_move_east(self) -> list[tuple[int]]:
        return [self.East,
                self.NorthEast,
                self.SouthEast]
    
    @property
    def req_move_west(self) -> list[tuple[int]]:
        return [self.West,
                self.NorthWest,
                self.SouthWest]

    def get_intended_dir(self, intend: 'Direction'):
        match intend:
            case Direction.North:
                return self.req_move_north, self.North
            case Direction.South:
                return self.req_move_south, self.South
            case Direction.East:
                return self.req_move_east, self.East
            case Direction.West:
                return self.req_move_west, self.West  

    def intent(self, elves: set, round: int):
        if not [point for point in self.adj_coords 
                                if Elf(point[0], point[1]) in elves]:
            return (self.x, self.y)
        round %= 4
        priority = (*self.priority[round:], *self.priority[:round])
        for dir in priority:
            req, pos = self.get_intended_dir(dir)
            if not [point for point in req 
                                if Elf(point[0], point[1]) in elves]:
                return pos
        return (self.x, self.y)

def get_min(elves: set, key):
    m = float('inf')
    for elf in elves:
        m = min(m, key(elf))
    return m

def get_max(elves: set, key):
    m = 0
    for elf in elves:
        m = max(m, key(elf))
    return m

def show(elves: set):
    x_min = get_min(elves, key=lambda elf: elf.x)-1
    y_min = get_min(elves, key=lambda elf: elf.y)-1

    x_max = get_max(elves, key=lambda elf: elf.x)+2
    y_max = get_max(elves, key=lambda elf: elf.y)+2

    for y in range(y_min, y_max):
        for x in range(x_min, x_max):
            print('#' if Elf(x,y) in elves
                    else '.', end='')
        print()
def get_ground_spaces(elves: set):
    x_min = get_min(elves, key=lambda elf: elf.x)
    y_min = get_min(elves, key=lambda elf: elf.y)

    x_max = get_max(elves, key=lambda elf: elf.x)
    y_max = get_max(elves, key=lambda elf: elf.y)

    return (x_max-x_min+1) * (y_max-y_min+1) - len(elves)

def first_half(elves: set, round: int):
    intentions = {}
    for elf in elves:
        intended = elf.intent(elves, round)
        intentions[intended] = intentions.get(intended, 0) + 1
    return intentions

def second_half(elves: set, round: int, intentions: dict):
    new_elves = set([])
    for elf in elves:
        intended = elf.intent(elves, round)
        if intentions[intended] != 1:
            new_elves.add(elf)
            continue
        new_elves.add(Elf(intended[0], intended[1]))
    return new_elves

def round(elves: set, round: int):
    intentions = first_half(elves, round)
    return second_half(elves, round, intentions)

input = [line.strip() for line in open('input.txt')]

elves = set([])
for y, line in enumerate(input):
    for x, symb in enumerate(line):
        if symb == '#':
            elves.add(Elf(x, y)) 
show(elves)
for i in range(10):
    print(f'round: {i+1}')
    elves = round(elves, i)
    #show(elves)

print(get_ground_spaces(elves))    