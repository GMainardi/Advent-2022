from enum import Enum, auto
class Mineral(Enum):
    ORE = auto()
    CLAY = auto()
    OBSIDIAN = auto()
    GEODE = auto()

    def __str__(self) -> str:
        return super().__str__().split('.')[1].lower()

class Factory:

    def __init__(self, desc: str) -> None:
        desc = desc.split()
        self.requirements = {}
        self.requirements[Mineral.ORE] = [(Mineral.ORE, int(desc[6]))]
        self.requirements[Mineral.CLAY] = [(Mineral.ORE, int(desc[12]))]
        self.requirements[Mineral.OBSIDIAN] = [(Mineral.ORE, int(desc[18])), (Mineral.CLAY, int(desc[21]))]
        self.requirements[Mineral.GEODE] = [(Mineral.ORE, int(desc[27])), (Mineral.OBSIDIAN, int(desc[30]))]
 
    def can_build(self, to_build: 'Mineral', resources: dict):
        return all([resources[mineral] >= qnt
                        for mineral, qnt in self.requirements[to_build]])

    def build_robot(self, to_build: 'Mineral', resources: dict):
        for mineral, qnt in self.requirements[to_build]:
            resources[mineral] -= qnt

    def max_ore_req(self):
        return max([req[0][1] for _, req in self.requirements.items()])
    
    def total_ore_req(self):
        return sum([req[0][1] for _, req in self.requirements.items()])
    
    def total_clay_req(self):
        return self.requirements[Mineral.OBSIDIAN][1][1]

    def total_obsidian_req(self):
        return self.requirements[Mineral.GEODE][1][1]
    
    def __str__(self) -> str:
        ans = ''
        for mat, req in self.requirements.items():
            ans += f'Each {mat} robot costs: ' + ' and '.join([f'{q} {m}' for m, q in req]) + '.\n'

        return ans
        

class State:

    def __init__(self, factory: 'Factory') -> None:
        self.storage = {Mineral.ORE:0, Mineral.CLAY:0, Mineral.OBSIDIAN:0, Mineral.GEODE:0}
        self.workers = {Mineral.ORE:1, Mineral.CLAY:0, Mineral.OBSIDIAN:0, Mineral.GEODE:0}
        self.min = 0
        self.factory = factory
    
    def add_worker(self, mineral: 'Mineral'):
        self.workers[mineral] = self.workers.get(mineral, 0) + 1

    def mine(self):
        for mineral, qnt in self.workers.items():
            self.storage[mineral] += qnt
    
    def new_robot_state(self, to_build: 'Mineral'):
        ns = State(self.factory)
        ns.storage = self.storage.copy()
        ns.workers = self.workers.copy()
        ns.min = self.min+1
        ns.factory = self.factory
        
        ns.factory.build_robot(to_build, ns.storage)
        ns.mine()
        ns.add_worker(to_build)
        return ns

    def new_mine_state(self):
        ns = State(self.factory)
        ns.storage = self.storage.copy()
        ns.workers = self.workers.copy()
        ns.min = self.min+1
        ns.factory = self.factory
        ns.mine()
        return ns

    def max_teorical_geode(self):
        r_time= 32-self.min
        return self.storage[Mineral.GEODE] + (self.workers[Mineral.GEODE] * r_time) + T(r_time)

    def next_states(self):
        max_time = 32

        if self.min == max_time:
            return []

        new_states = []

        if self.factory.can_build(Mineral.GEODE, self.storage):
            return [self.new_robot_state(Mineral.GEODE)]

        if self.factory.can_build(Mineral.OBSIDIAN, self.storage):
            new_states.append(self.new_robot_state(Mineral.OBSIDIAN))

        if self.factory.can_build(Mineral.CLAY, self.storage):
            if self.workers[Mineral.CLAY] < self.factory.total_clay_req():
                new_states.append(self.new_robot_state(Mineral.CLAY))
        
        if self.factory.can_build(Mineral.ORE, self.storage):
            if self.workers[Mineral.ORE] < self.factory.max_ore_req():
                new_states.append(self.new_robot_state(Mineral.ORE))

        
        if self.storage[Mineral.ORE] < self.factory.max_ore_req()*2 - (self.workers[Mineral.ORE]):
            new_states.append(self.new_mine_state())

        return new_states

    def value(self):
        return self.storage[Mineral.GEODE]

def T(n: int):
    return ((n**2)+2)/2.0

def DFS(curr: 'State'):
    global best

    if not curr.next_states():
        return curr.value()

    for child in curr.next_states():
        if curr.max_teorical_geode() < best:
            continue
        best = max(best, DFS(child))
    
    return best

input = [line.strip() for line in open('input.txt')][:3]
total = 1
for idx, line in enumerate(input): # 5 min-ish m1 air 
    best = 0
    initial_state = State(Factory(line))
    m = DFS(initial_state)
    print(m)
    total *= m
print(total)