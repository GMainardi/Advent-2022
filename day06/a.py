input = open('input.txt').readline()

start = 0
end = 4
marker = set(input[start:end])
while len(marker) < 4:
    start += 1
    end += 1
    marker = set(input[start:end])

print(end)