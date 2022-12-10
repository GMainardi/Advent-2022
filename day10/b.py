from enum import Enum
from dataclasses import dataclass

class operator(Enum):
    NOOP = 0
    ADDX = 1

@dataclass
class command():
    op: operator
    value: int = float('inf')

def convert_command(cm):
    cm = cm.split( )
    if cm[0] == 'addx':
        return command(operator.ADDX, int(cm[1]))
    return command(operator.NOOP)

def signal_strength(x_reg, cicle):
    return x_reg * cicle

program = list(map(convert_command, [line.strip() for line in open('input.txt')]))



CTR = ''
CTR_count = 0
pc = 0
cicle = 1
x_reg = 1
sum = None

while pc < len(program):

    if CTR_count in [x_reg-1, x_reg, x_reg+1]:
        CTR += '#'
    else:
        CTR += '.'

    cmd = program[pc]

    if cmd.op == operator.NOOP:
        cicle += 1
        pc += 1

    elif cmd.op == operator.ADDX:
        cicle += 1

        if sum is None:
            sum = x_reg + cmd.value
        else:
            x_reg = sum
            sum = None
            pc += 1

    CTR_count += 1
    if CTR_count % 40 == 0:
        CTR_count = 0
        CTR += '\n'

print(CTR)