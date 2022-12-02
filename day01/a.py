input = [line.strip() for line in open('input.txt', 'r')]


partial = 0
max_global_sum = 0

for line in input:

    if line != '':
        partial += int(line)
        
    else:
        if partial >= max_global_sum:
            max_global_sum = partial
        partial = 0
else:
    if partial >= max_global_sum:
            max_global_sum = partial

print(max_global_sum)
    