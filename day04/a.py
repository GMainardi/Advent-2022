def fully_inside(pair):
    first, second = pair
    print(pair)
    if first[0] < second[0]:
        return fully_inside((second, first))
    return (first[0] >= second[0] and first[1] <= second[1]) or \
           (second[0] >= first[0] and second[1] <= first[1])

input = [((int(line.split(',')[0].split('-')[0]), int(line.split(',')[0].split('-')[1])),
          (int(line.split(',')[1].split('-')[0]), int(line.split(',')[1].split('-')[1])))
          for line in open('input.txt')]

print(sum(map(fully_inside, input)))