def check_up(m, x, y):
    tree_size = m[x][y]
    up = [line[y] for line in m[:x]]
    if not len(up):
        return True
    return max(up) < tree_size 

def check_down(m, x, y):
    tree_size = m[x][y]
    down = [line[y] for line in m[x+1:]]
    if not len(down):
        return True
    return max(down) < tree_size

def check_right(m, x, y):
    tree_size = m[x][y]
    right = m[x][y+1:]
    if not len(right):
        return True
    return max(right) < tree_size

def check_left(m, x, y):
    tree_size = m[x][y]
    left = m[x][:y]
    if not len(left):
        return True
    return max(left) < tree_size

def is_visible(m, x, y):
    return check_up(m, x, y) or check_down(m, x, y) \
        or check_left(m, x, y) or check_right(m, x, y)

def print_hightlight(m, visibles):
    for x in range(len(m)):
        for y in range(len(m[x])):
            if (x, y) in visibles:
                print('\033[93m', end='')
            else:
                print('\033[0m', end='')
            print(f'{m[x][y]} ', end='')
        print()

input = [list(map(lambda x : int(x), line.strip())) for line in open('input.txt')]

visible = 0
visibles = []
for x in range(len(input)):
    for y in range(len(input[x])):
        vis = is_visible(input, x, y)
        if vis:
            visibles.append((x, y))
        visible += int(is_visible(input, x, y))
print(visible)
