def fully_inside(pair):
    first, second = pair
    start = max(first[0], second[0])
    end = min(first[1], second[1])
    return end >= start

input = [((int(line.split(',')[0].split('-')[0]), int(line.split(',')[0].split('-')[1])),
          (int(line.split(',')[1].split('-')[0]), int(line.split(',')[1].split('-')[1])))
          for line in open('input.txt')]

print(sum(map(fully_inside, input)))