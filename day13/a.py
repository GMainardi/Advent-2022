from ast import literal_eval

def compare(pair, lvl = 0):

    left, right = pair

    print('  ' * lvl, end='')
    print(f'- Compare {left} vs {right}')
    
    if type(left) == int and type(right) == int:
        return right - left

    if len(left) and not len(right):
        return -1

    for l, r in zip(left, right):
        if type(l) == list and type(r) == int:
            comp = compare((l, [r]), lvl+1)
        elif type(l) == int and type(r) == list:
            comp = compare(([l], r), lvl+1)
        else:
            comp = compare((l, r), lvl+1)

        if comp > 0:
            return 1

        elif comp < 0:
            return -1

    return len(right) - len(left)

with open('input.txt') as file:
    input = file.read().split('\n\n')

pairs = [(literal_eval(line.split('\n')[0]), literal_eval(line.split('\n')[1])) for line in input]

print(pairs)

s = 0
right = []
for i, pair in enumerate(pairs):
    c = compare(pair)
    print(c)
    if c >= 0:  
        print('gremio')
        right.append(i+1)
        s+= i+1
    print()
print(right)
print(s)