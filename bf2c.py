#!/usr/bin/env python3

#This script converts a Brainfuck source to a C source.

import sys

def print_usage() -> None:
    print("Usage: ./bf2c.py <input Brainfuck source> <output C source>")
    sys.exit(0)

if (len(sys.argv) != 3):
    print_usage()

bf_source: str = sys.argv[1]
c_source: str = sys.argv[2]

if ((not bf_source.endswith('.brainf')) or (not c_source.endswith('.c')) or (bf_source.startswith('-'))):
    print_usage()

bf_source_content: str = ""
with open(bf_source, 'r') as f:
    bf_source_content = f.read()
bf_source_content += ' '

with open(c_source, 'w') as f:

    indent: int = 0

    def put(s: str = '') -> None:
        for i in range(indent):
            f.write('    ')
        f.write(s + '\n')

    put('#include <stdio.h>')
    put('#include "./brainfuck.h"')
    put()
    put('int main(void) {')
    put()

    indent += 1

    pc: str = None #previous command
    num_repeat: int = 1

    for i in range(len(bf_source_content)):

        c: str = bf_source_content[i]

        if (pc is not None):
            if (c == pc):
                num_repeat += 1
            else:
                if (pc == '>'):
                    if (num_repeat == 1):
                        put('++ptr;')
                    else:
                        put(f'ptr += {num_repeat};')
                elif (pc == '<'):
                    if (num_repeat == 1):
                        put('--ptr;')
                    else:
                        put(f'ptr -= {num_repeat};')
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

print('Conversion succeeded.')
print(f'[ {bf_source} ] -> [ {c_source} ]')

