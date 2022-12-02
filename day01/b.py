input = [line.strip() for line in open('input.txt', 'r')]


partial = 0
max_global_sum = [0, 0, 0]

for line in input:

    if line != '':
        partial += int(line)

    else:
        if partial >= min(max_global_sum):
            max_global_sum[2] = partial
            max_global_sum = sorted(max_global_sum, reverse=True)


        partial = 0
else:
    if partial >= min(max_global_sum):
        max_global_sum[2] = partial
        max_global_sum = sorted(max_global_sum, reverse=True)


print(sum(max_global_sum))
    