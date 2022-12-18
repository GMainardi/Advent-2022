class Cube:

    def __init__(self, line) -> None:
        self.x, self.y, self.z = [int(n) for n in line.split(',')]

    def __repr__(self) -> str:
        return f'x: {self.x} y: {self.y} z: {self.z}'

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Cube):
            return False
        
        return (self.x, self.y, self.z) == (__o.x, __o.y, __o.z)

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def adj_cubes(self):
        return set([Cube(f'{self.x+1},{self.y  },{self.z  }'),
                    Cube(f'{self.x-1},{self.y  },{self.z  }'),
                    Cube(f'{self.x  },{self.y+1},{self.z  }'),
                    Cube(f'{self.x  },{self.y-1},{self.z  }'),
                    Cube(f'{self.x  },{self.y  },{self.z+1}'),
                    Cube(f'{self.x  },{self.y  },{self.z-1}')])

    def blocking_sides(self, lava):
        count = 0
        for cube in self.adj_cubes():
            if cube in lava:
                count += 1
        return count
            
lava = set([Cube(line.strip()) for line in open('input.txt')])

total_blocked = 0
for cube in lava:
    total_blocked += cube.blocking_sides(lava)

print(len(lava)*6 - total_blocked)