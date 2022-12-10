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


total_strength = 0
lookupsignals = [20, 60, 100, 140, 180, 220]

pc = 0
cicle = 1
x_reg = 1
sum = None

while pc < len(program):
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

    if cicle in lookupsignals:
        total_strength += signal_strength(x_reg, cicle)
        print(f'X: {x_reg}')
        print(f'cicle: {cicle}')
        print(f'signal strength: {signal_strength(x_reg, cicle)}')
        print(f'toal strength: {total_strength}')
