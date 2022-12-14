def create_hor_slice(slc1, slc2):
    rocks = set([])
    for i in range(slc1[0], slc2[0]+1):
        rocks.add((i, slc1[1]))
    
    return rocks
    
def create_ver_slice(slc1, slc2):
    rocks = set([])
    for i in range(slc1[1], slc2[1]+1):
        rocks.add((slc1[0], i))
    
    return rocks

def create_rocks(slc1, slc2):
    if slc1[0] > slc2[0] or slc1[1] > slc2[1]:
        return create_rocks(slc2, slc1)
    
    if slc1[0] != slc2[0]:
        return create_hor_slice(slc1, slc2)
    elif slc1[1] != slc2[1]:
        return create_ver_slice(slc1, slc2)
    
def print_rocks(rocks):
    start_x = min(rocks, key=lambda x: x[0])[0]
    end_x = max(rocks, key=lambda x: x[0])[0]

    start_y = min(rocks, key=lambda x: x[1])[1]
    end_y = max(rocks, key=lambda x: x[1])[1]

    for y in range(start_y, end_y+1):
        for x in range(start_x, end_x+1):  
            if (x, y) in rocks:
                print('#', end='')
            else:
                print('.', end='')
        print()

def drop_sand(rocks):
    sand = (500, 0)
    abyss = max(rocks, key=lambda x: x[1])[1]
    while sand[1] <= abyss:

        down = (sand[0], sand[1]+1)
        left = (sand[0]-1, sand[1]+1)
        right = (sand[0]+1, sand[1]+1)

        if  down not in rocks:
            sand = down
        elif left not in rocks:
            sand = left
        elif right not in rocks:
            sand = right
        else:
            return sand, False

    return sand, True
        
input = [[(int(slc.split(',')[0]),int(slc.split(',')[1])) for slc in line.strip().split(' -> ')] for line in open('input.txt')]

rocks = set([])
for draw_rocks in input:
    for start, end in zip(draw_rocks[:-1], draw_rocks[1:]):
        rocks = rocks.union(create_rocks(start, end))

s_rocks = len(rocks)

sand, last = drop_sand(rocks)
while not last:
    rocks.add(sand)
    sand, last = drop_sand(rocks)

print_rocks(rocks)

print(len(rocks)-s_rocks)