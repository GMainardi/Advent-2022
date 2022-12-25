def SNAFU_to_decimal(number: str):
    curr_pow = len(number)-1
    total = 0
    for num in number:
        curr_mult = 5**curr_pow
        curr_pow -=1
        match num:
            case '-':
                total -= 1 * curr_mult
            case '=':
                total -= 2 * curr_mult
            case _:
                total += int(num) * curr_mult
    return total

def decimal_to_SNAFU(number: int):
    ans = ''
    while number != 0:
        match number%5:
            case 4:
                ans += '-'
                number += 1
            case 3:
                ans += '='
                number += 2
            case other:
                ans += str(other)
        number //=5
    return ans[::-1]

print(decimal_to_SNAFU(sum([SNAFU_to_decimal(line.strip()) 
                            for line in open('input.txt')])))