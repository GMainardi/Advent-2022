from dataclasses import dataclass, field
from tqdm import tqdm

@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

@dataclass()
class Shape:
    points: set[Point]

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
        self.points = set([Point(p.x, p.y+1) for p in self.points])
    
    def move(self, direction, floor):
        if not self.can_move(direction, floor):
            return
        self.points = set([Point(p.x+direction, p.y) for p in self.points])

    @property
    def highest_point(self):
        highest = 0
        for p in self.points:
            highest = min(p.y, highest)
        return highest

class Fblock(Shape):

    def __init__(self, highest) -> None:

        start_points = set([Point(2, 0), Point(3, 0), Point(4, 0), Point(5, 0)])
        start_points = set([Point(p.x, p.y + highest - 4) for p in start_points])
        super().__init__(start_points)
    
class Pblock(Shape):

    def __init__(self, highest) -> None:

        start_points = set([Point(3, -2), Point(2, -1), Point(3, -1), Point(4, -1), Point(3, 0)])
        start_points = set([Point(p.x, p.y + highest - 4) for p in start_points])
        super().__init__(start_points)
    
class Jblock(Shape):

    def __init__(self, highest) -> None:

        start_points = set([Point(4, -2), Point(4, -1), Point(2, 0), Point(3, 0), Point(4, 0)])
        start_points = set([Point(p.x, p.y + highest - 4) for p in start_points])

        super().__init__(start_points)
    
class Iblock(Shape):

    def __init__(self, highest) -> None:

        start_points = set([Point(2, -3), Point(2, -2), Point(2, -1), Point(2, 0)])
        start_points = set([Point(p.x, p.y + highest - 4) for p in start_points])

        super().__init__(start_points)
    
class Oblock(Shape):

    def __init__(self, highest) -> None:

        start_points = set([Point(2, -1), Point(2, 0), Point(3, -1), Point(3, 0)])
        start_points = set([Point(p.x, p.y + highest - 4) for p in start_points])

        super().__init__(start_points)

class Moves:

    def __init__(self, fname) -> None:
        self.moves = [1 if s == '>' else -1 for s in open(fname).readlines()[0].strip()]
        self.id = 0
    
    def get_next(self):
        next_move = self.moves[self.id]
        self.id = (self.id+1) % len(self.moves)
        return next_move
    
def get_next_shape(round, highest):
    round %= 5
    match round:
        case 0:
            return Fblock(highest)
        case 1:
            return Pblock(highest)
        case 2:
            return Jblock(highest)
        case 3:
            return Iblock(highest)
        case 4:
            return Oblock(highest)

    return None

moves = Moves('input.txt')
floor = set([Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0), Point(4, 0), Point(5, 0), Point(6, 0)])

highest = 0
rock = 0
rock_to_drop = 1_000_000_000_000
cache = {}
while rock < rock_to_drop:

    seen = (rock%5, moves.id)
    if seen in cache:
        period = rock - cache[seen][0]
        if rock % period == rock_to_drop % period:
            stored_h = cache[seen][1]
            period_h = abs(highest) - stored_h
            period_ocr = ((rock_to_drop-rock)//period) + 1
            print(stored_h + period_h * period_ocr)
            break
    else:
        cache[seen] = rock, abs(highest)
    
    shape = get_next_shape(rock, highest)

    shape.move(moves.get_next(), floor)

    while shape.can_drop(floor):
        shape.drop()
        shape.move(moves.get_next(), floor)


    floor = floor.union(shape.points)
       
    highest = min(highest, shape.highest_point)

    rock += 1
