from ast import literal_eval
from functools import cmp_to_key

def compare(left, right):
 
    if type(left) == int and type(right) == int:
        return right - left

    if len(left) and not len(right):
        return -1

    for l, r in zip(left, right):
        if type(l) == list and type(r) == int:
            comp = compare(l, [r])
        elif type(l) == int and type(r) == list:
            comp = compare([l], r)
        else:
            comp = compare(l, r)

        if comp > 0:
            return 1

        elif comp < 0:
            return -1

    return len(right) - len(left)

pairs = [literal_eval(line.strip()) for line in open('input.txt') if line != '\n']

sorted_p = sorted(pairs, key=cmp_to_key(compare), reverse=True)

pack1 = [[2]]
pack2 = [[6]]
p1_i = 0
p2_i = 0
for i, val in enumerate(sorted_p):
    if compare(pack1, val) == 1:
        p1_i = i+1
        break
for i in range(p1_i, len(sorted_p)):
    if compare(pack2, sorted_p[i]) == 1:
        p2_i = i+2
        break

print(p1_i*p2_i)