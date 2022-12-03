def find_commum(line):
    first_part, segund_part = line
    for char in first_part:
        if char in segund_part:
            return  ord(char) - 38 if char.upper() == char else ord(char)-96

input = [(line.strip()[len(line.strip())//2:], line.strip()[:len(line.strip())//2]) for line in open('input_test.txt')]


print(sum(map(find_commum, input)))