import re 

def split_list(list, elem):
    break_point = list.index(elem)
    return list[:break_point], list[break_point:]

def get_inst_values(inst):
    return [int(m) for m in re.findall('[0-9]+', inst)]

input = [line for line in open('input.txt')]

pilhas = []
first_part, second_part = split_list(input, '\n')

for line in first_part:
    matches = [m.start(0) for m in re.finditer('[A-Z]', line)]
    for match in matches:
        index_pilha = ((match - 1) // 4)
        while  index_pilha > len(pilhas) - 1:
            pilhas.append([])
        pilhas[index_pilha].append(line[match])

for line in second_part[1:]:
    n, src, dst = get_inst_values(line)
    for i in range(n):
        pilhas[dst-1].insert(0, pilhas[src-1].pop(0))

answ = ''
for pilha in pilhas:
    answ += pilha[0]

print(answ)