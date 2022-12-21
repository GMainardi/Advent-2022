
def value(r_name, rules):
    if type(rules[r_name]) == int:
        return rules[r_name]

    first_value = value(rules[r_name][0], rules)
    op = rules[r_name][1]
    second_value = value(rules[r_name][2], rules)
    return eval(f'{first_value} {op} {second_value}')

rules = {}
with open('input.txt', 'r') as file:
    for line in file.readlines():
        rule = line.strip().split(':')
        try:
            rules[rule[0]] = int(rule[1])
        except ValueError:
            rules[rule[0]] = rule[1][1:].split()

print(value('root', rules))