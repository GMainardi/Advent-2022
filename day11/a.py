class WorryLevelCalculator:

    def __init__(self, description: list, old: int):
        self.old = old
        self.calc = "".join([item if item != 'old' else str(old) for item in description])
                
    def eval(self):
        return eval(self.calc)
        
class Monkey:

    def __init__(self, description):
        infos = description.split('\n')
        self.id = int(infos[0].split()[1][:-1])
        self.items = [int(item) for item in infos[1].replace(' ', '').split(':')[1].split(',')]
        self.calc = infos[2].split()[3:]
        self.test = int(infos[3].split()[-1])
        self.succed = int(infos[4].split()[-1])
        self.fail = int(infos[5].split()[-1])
        self.insp_count = 0

    def analysis_item(self, item):
        self.insp_count += 1
        # print(f'\tMonkey inspects an item with a worry level of {item}.')
        worry_level = WorryLevelCalculator(self.calc, item).eval()
        # print(f'\t\tWorry level is {worry_level}.')
        worry_level = worry_level // 3
        # print(f'\t\tMonkey gets bored with item. Worry level is divided by 3 to {worry_level}.')
        
        if worry_level % self.test == 0:
            # print(f'Current worry level is divisible by {self.test}.')
            # print(f'Item with worry level {worry_level} is thrown to monkey {self.succed}.')
            return (self.succed, worry_level)
        else:
            # print(f'Current worry level is not divisible by {self.test}.')
            # print(f'Item with worry level {worry_level} is thrown to monkey {self.fail}.')
            return (self.fail, worry_level)
              
    def round(self):
        to_throw =  [self.analysis_item(item) for item in self.items]
        self.items = []
        return to_throw

    def receve_item(self, item):
        self.items.append(item)

    def __repr__(self) -> str:
        return f'Monkey {self.id}: {self.items}'

    def __str__(self) -> str:
        return f"""Monkey {self.id}:
  Starting items: {self.items}
  Operation: new = {' '.join(self.calc)}
  Test: divisible by {self.test}
    If true: throw to monkey {self.succed}
    If false: throw to monkey {self.fail}\n"""


with open('input.txt', 'r') as file:
    input = file.read()

monkeys = [Monkey(m) for m in input.split('\n\n')]

for i in range(20):
    print(f'round {i}: ')
    for monkey in monkeys:
        throwing_items = monkey.round()
        for dest, item in throwing_items:
            monkeys[dest].receve_item(item)
    
    for monkey in monkeys:
        print(f'\t{repr(monkey)}')

most_actives = [0, 0]
for monkey in monkeys:
    if monkey.insp_count > most_actives[0]:
        most_actives[0] = monkey.insp_count
        most_actives.sort()

print(most_actives[0]*most_actives[1])