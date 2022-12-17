from dataclasses import dataclass
from tqdm import tqdm

@dataclass(order=True)
class Point:
    x: int
    y: int

@dataclass()
class Shape:
    points: list[Point]


    def can_drop(self, floor):
        for p in self.points:
            if Point(p.x, p.y+1) in floor:
                return False
        return True

    def can_move(self, direction, floor):
        for p in self.points:
            if p.x+direction < 0 or p.x+direction > 6:
                return False
            if Point(p.x+direction, p.y) in floor:
                return False
        return True

    def drop(self):
        for p in self.points:
            p.y += 1
    
    def move(self, direction, floor):
        if not self.can_move(direction, floor):
            return
        for p in self.points:
            p.x += direction
        
    def __str__(self) -> str:
        s_x = sorted(self.points, key=lambda item: item.x)[0].x
        s_y = sorted(self.points, key=lambda item: item.y)[0].y

        e_x = sorted(self.points, key=lambda item: item.x)[-1].x
        e_y = sorted(self.points, key=lambda item: item.y)[-1].y

        ans = ''
        for y in range(s_y, e_y+1):
            for x in range(s_x, e_x+1):
                if Point(x, y) in self.points:
                    ans += '@'
                else:
                    ans += ' '
            ans += '\n'
        return ans

class Fblock(Shape):

    def __init__(self) -> None:

        start_points = [Point(2, 0), Point(3, 0), Point(4, 0), Point(5, 0)]

        super().__init__(start_points)
    
class Pblock(Shape):

    def __init__(self) -> None:

        start_points = [Point(3, -2), Point(2, -1), Point(3, -1), Point(4, -1), Point(3, 0)]

        super().__init__(start_points)
    
class Jblock(Shape):

    def __init__(self) -> None:

        start_points = [Point(4, -2), Point(4, -1), Point(2, 0), Point(3, 0), Point(4, 0)]

        super().__init__(start_points)
    
class Iblock(Shape):

    def __init__(self) -> None:

        start_points = [Point(2, -3), Point(2, -2), Point(2, -1), Point(2, 0)]

        super().__init__(start_points)
    
class Oblock(Shape):

    def __init__(self) -> None:

        start_points = [Point(2, -1), Point(2, 0), Point(3, -1), Point(3, 0)]

        super().__init__(start_points)

class Moves:

    def __init__(self, fname) -> None:
        self.moves = [1 if s == '>' else -1 for s in open(fname).readlines()[0].strip()]
        self.id = 0
    
    def get_next(self):
        self.id += 1
        return self.moves[(self.id-1) % len(self.moves)]
    
def get_next_shape(round):
    round %= 5
    match round:
        case 0:
            return Fblock()
        case 1:
            return Pblock()
        case 2:
            return Jblock()
        case 3:
            return Iblock()
        case 4:
            return Oblock()

    return None

def update_floor(floor, shape):
    start = sorted(floor, key=lambda item: item.y)[0].y
    floor = [*floor, *shape.points]
    end = sorted(floor, key=lambda item: item.y)[0].y
    for p in floor:
        p.y += (start - end)
    return (start - end), floor

def print_result(floor):
    s_x = sorted(floor, key=lambda item: item.x)[0].x
    s_y = sorted(floor, key=lambda item: item.y)[0].y

    e_x = sorted(floor, key=lambda item: item.x)[-1].x
    e_y = sorted(floor, key=lambda item: item.y)[-1].y

    ans = ''
    for y in range(s_y, e_y+1):
        for x in range(s_x, e_x+1):
            if Point(x, y) in floor:
                ans += '#'
            else:
                ans += '.'
        ans += '\n'
    print(ans)

moves = Moves('input.txt')
floor = [Point(0, 4), Point(1, 4), Point(2, 4), Point(3, 4), Point(4, 4), Point(5, 4), Point(6, 4)]
total = 0
for round in tqdm(range(2022)):
    shape = get_next_shape(round)

    shape.move(moves.get_next(), floor)
    while shape.can_drop(floor):
        shape.drop()
        shape.move(moves.get_next(), floor)

    down, floor = update_floor(floor, shape)
    total += down
print(total)
print('\n')