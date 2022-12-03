def find_commum(l1, l2, l3):
    for char in l1:
        if char in l2 and char in l3:
            return  ord(char) - 38 if char.upper() == char else ord(char)-96

input = [line.strip() for line in open('input.txt')]

total = 0
for index in range(0, len(input), 3):
    total += find_commum(input[index],
                       input[index+1],
                       input[index+2])

print(total)