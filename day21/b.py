from sympy import solve

def value(r_name, rules):
    if r_name == 'humn':
        return 'humn'
    if type(rules[r_name]) == int:
        return str(rules[r_name])

    first_value = value(rules[r_name][0], rules)
    op = rules[r_name][1]
    second_value = value(rules[r_name][2], rules)
    return f'({first_value} {op} {second_value})'

def eval_root(rules):
    first_part = value(rules['root'][0], rules)
    second_part = eval(value(rules['root'][2], rules))
    eq = f'{first_part} - {second_part}'
    ans = solve(eq)[0]
    return int(ans)


rules = {}
with open('input.txt', 'r') as file:
    for line in file.readlines():
        rule = line.strip().split(':')
        try:
            rules[rule[0]] = int(rule[1])
        except ValueError:
            rules[rule[0]] = rule[1][1:].split()

print(eval_root(rules))