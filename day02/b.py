def cal_points(play):
    oponent, you = play
    match oponent:
        case 'A':
            match you:
                case 'X':
                    return 3 + 0
                case 'Y':
                    return 1 + 3
                case 'Z':
                    return 2 + 6
        case 'B':
            match you:
                case 'X':
                    return 1 + 0
                case 'Y':
                    return 2 + 3
                case 'Z':
                    return 3 + 6
        case 'C':
            match you:
                case 'X':
                    return 2 + 0
                case 'Y':
                    return 3 + 3
                case 'Z':
                    return 1 + 6 
    
input = [(line.strip().split(' ')[0], line.strip().split(' ')[1]) for line in open('input.txt')]


print(sum(map(cal_points, input)))