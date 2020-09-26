#!/usr/bin/env python3

#An interpreter for yBrainfuck 1.x.
#Algorithm:
#1. Converts the specified yBrainfuck source `A.brainf` to a C source `A.brainf.c`.
#2. Compiles `A.brainf.c` using `gcc` and executes it.

import subprocess
import sys

def print_usage() -> None:
    print("Usage: ybrainfuck <source>.brainf")
    sys.exit(0)

if ((len(sys.argv) != 2) or (len(sys.argv) != 1 and sys.argv[1].startswith('-'))):
    print_usage()

input_source_file: str = sys.argv[1]
output_source_extension: str = '.c'
output_source_file: str = input_source_file + output_source_extension

input_source: list = []
with open(input_source_file, 'r') as f:
    input_source = f.readlines()
if (input_source[0].startswith('[')): #ignores the first comment line if exists
    input_source[0] = ''
for i in range(len(input_source)): #ignores comment lines
    j: int = input_source[i].find('#')
    if (j != -1):
        input_source[i] = input_source[i][:j]
input_source: str = ''.join(input_source) + ' '

with open(output_source_file, 'w') as f:

    indent: int = 0

    def put(s: str = '') -> None:
        for i in range(indent):
            f.write('    ')
        f.write(s + '\n')

    put('#include <stdio.h>')
    put()
    put('unsigned char __data[30000] = {0};')
    put('char *ptr = __data;')
    put()
    put('int main(void) {')
    put()

    indent += 1

    pc: str = None #previous command
    num_repeat: int = 1

    position: int = 0
    position_dict: dict = {}
    for i, j in enumerate('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        position_dict[j] = i

    for i in range(len(input_source)):

        c: str = input_source[i]

        if (pc is not None):
            if (c == pc):
                num_repeat += 1
            else:
                if (pc in position_dict):
                    position_diff: int = position_dict[pc] - position
                    if (position_diff > 0):
                        pc = '>'
                        num_repeat = position_diff
                    elif (position_diff < 0):
                        pc = '<'
                        num_repeat = abs(position_diff)

                if (pc == '>'):
                    if (num_repeat == 1):
                        put('++ptr;')
                    else:
                        put(f'ptr += {num_repeat};')
                    position += num_repeat
                elif (pc == '<'):
                    if (num_repeat == 1):
                        put('--ptr;')
                    else:
                        put(f'ptr -= {num_repeat};')
                    position -= num_repeat
                elif (pc == '+'):
                    if (num_repeat == 1):
                        put('++*ptr;')
                    else:
                        put(f'*ptr += {num_repeat};')
                elif (pc == '-'):
                    if (num_repeat == 1):
                        put('--*ptr;')
                    else:
                        put(f'*ptr -= {num_repeat};')
                elif (pc == '.'):
                    for i in range(num_repeat):
                        put('putchar(*ptr);')
                elif (pc == ','):
                    for i in range(num_repeat):
                        put('*ptr = getchar();')
                elif (pc == '['):
                    for i in range(num_repeat):
                        put('while (*ptr) {')
                        indent += 1
                elif (pc == ']'):
                    for i in range(num_repeat):
                        indent -= 1
                        put('}')

                num_repeat = 1

        pc = c

    indent -= 1

    put()
    put('}')
    put()

binary_file: str = output_source_file.replace(output_source_extension, '.out')

subprocess.run([
        'gcc',
        output_source_file,
        '-o',
        binary_file,
    ],
    check = True
)

subprocess.run([
        binary_file,
    ],
    check = True,
)

