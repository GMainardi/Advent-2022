import itertools
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

    def adj_cubes(self, lim = float('inf')):
        return set(filter(lambda x: x.inside_lim(lim), [Cube(f'{self.x+1},{self.y  },{self.z  }'),
                    Cube(f'{self.x-1},{self.y  },{self.z  }'),
                    Cube(f'{self.x  },{self.y+1},{self.z  }'),
                    Cube(f'{self.x  },{self.y-1},{self.z  }'),
                    Cube(f'{self.x  },{self.y  },{self.z+1}'),
                    Cube(f'{self.x  },{self.y  },{self.z-1}')]))

    def inside_lim(self, lim):
        return -1 <= self.x <= lim \
           and -1 <= self.y <= lim \
           and -1 <= self.z <= lim

    def blocking_sides(self, lava):
        count = 0
        for cube in self.adj_cubes():
            if cube in lava:
                count += 1
        return count

class Lava:

    def __init__(self, cubes) -> None:
        self.cubes = cubes
        self.lim = 0
        for cube in cubes:
            self.lim = max(self.lim, cube.x, cube.y, cube.z)
        self.lim += 1

    def outside_lava(self):
        starter_cube = Cube('0,0,0')
        queue = [starter_cube]
        water = set([])

        while queue:
            curr = queue.pop(0)
            if curr in water:
                continue
            water.add(curr)
            for adj in curr.adj_cubes(self.lim):
                if adj not in lava.cubes:
                    queue.append(adj)

        return water
    

lava = Lava(set([Cube(line.strip()) for line in open('input.txt')]))

water = lava.outside_lava()

outside_sides = 0
for cube in lava.cubes:

    outside_sides += cube.blocking_sides(water)

print(outside_sides)