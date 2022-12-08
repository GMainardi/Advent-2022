def check_up(m, x, y):
    tree_size = m[x][y]
    up = [line[y] for line in m[:x]][::-1]
    total = 0
    for tree in up:
        total += 1
        if tree >= tree_size:
            break
    return total

def check_down(m, x, y):
    tree_size = m[x][y]
    down = [line[y] for line in m[x+1:]]
    total = 0
    for tree in down:
        total += 1
        if tree >= tree_size:
            break
    return total

def check_right(m, x, y):
    tree_size = m[x][y]
    right = m[x][y+1:]
    total = 0
    for tree in right:
        total += 1
        if tree >= tree_size:
            break
    return total

def check_left(m, x, y):
    tree_size = m[x][y]
    left = m[x][:y][::-1]
    total = 0
    for tree in left:
        total += 1
        if tree >= tree_size:
            break
    return total

def tree_house_score(m, x, y):
    up_score = check_up(m, x, y)
    down_score = check_down(m, x, y)
    left_score = check_left(m, x, y)
    right_score = check_right(m, x, y)
    return  up_score * down_score \
        * right_score * left_score

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

best_spot_view = -1
for x in range(len(input)):
    for y in range(len(input[x])):
        curr_tree_score = tree_house_score(input, x, y)
        if curr_tree_score > best_spot_view:
            best_spot_view = curr_tree_score

print(best_spot_view)
