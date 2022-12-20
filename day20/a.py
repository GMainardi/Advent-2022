def mix(file):
    it = 0
    while it < len(file):
        if file[it][1]:
            it += 1
        else:
            val, _ = file.pop(it)
            pos = (it+val)%len(file)
            file.insert(pos, (val, True))
            it = 0

def grove_coords(file):
    start = file.index((0, True))
    fst, _ = file[(start+1000)%len(file)]
    scd, _ = file[(start+2000)%len(file)]
    trd, _ = file[(start+3000)%len(file)]

    return fst + scd + trd

input = [(int(line.strip()), False) for line in open('input.txt')]

mix(input)
print(grove_coords(input))