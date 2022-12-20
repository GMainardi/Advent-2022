def mix(mirror, file):
    for item in mirror:
        f_idx = file.index(item)
        val, id = file.pop(f_idx)
        pos = (f_idx+val)%len(file)
        file.insert(pos, (val, id))

def grove_coords(file, zero):
    start = file.index(zero)
    fst = (start+1000)%len(file)
    scd = (fst+1000)%len(file)
    trd = (scd+1000)%len(file)

    fst = file[fst][0]
    scd = file[scd][0]
    trd = file[trd][0]
    return fst + scd + trd

key = 811589153
input = []
mirror = []
with open('input.txt', 'r') as file:
    for line in file.readlines():
        num = int(line.strip())
        input.append((num*key, len(input)))
        if num == 0:
            zero = input[-1]

mirror = input.copy()
for _ in range(10):
    mix(mirror, input)
print(grove_coords(input, zero))