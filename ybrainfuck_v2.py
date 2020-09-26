#!/usr/bin/env python3

#An interpreter for yBrainfuck 2.x.
version: str = '2.0.0'

#-------------------------------------#

### import ###

import os
import re
import subprocess
import sys

#-------------------------------------#

### Classes ###

class BrainFuckArray:

    def __init__(self, variable_list: set) -> None:

        self.data:          list = []

        #unsigned char
        self.min_value:     int  = 0
        self.max_value:     int  = 255

        self.min_position:  int  = 0
        self.max_position:  int  = 30000 - 1

        self.position:               int  = 0
        self.position_dict:          dict = {}
        self.position_dict_reversed: dict = {} #for `self.printStructure()`

        for i in range(self.max_position - self.min_position + 1):
            self.data.append(0)

        builtin_variables: str = 'abcdefghijklmnopqrstuvwxyz' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i, char in enumerate(builtin_variables):
            self.position_dict[char] = i
            self.position_dict_reversed[i] = char
        for i, variable_name in enumerate(variable_list, start = len(builtin_variables)):
            self.position_dict[variable_name] = i
            self.position_dict_reversed[i] = variable_name

    def forward(self, num_shift: int = 1) -> None:
        self.position += num_shift
        if (self.position > self.max_position):
            raise Exception(f'Buffer overrun occurred. The current position [ {self.position} ] exceeds `{self.max_position}`.')

    def backward(self, num_shift: int = 1) -> None:
        self.position -= num_shift
        if (self.position < self.min_position):
            raise Exception(f'Buffer overrun occurred. The current position has the negative value [ {self.position} ].')

    def moveTo(self, variable_name: str) -> None:
        if (variable_name not in self.position_dict):
            raise Exception(f'The variable [ {variable_name} ] is not defined.')
        position_diff: int = self.position_dict[variable_name] - self.position
        if (position_diff > 0):
            self.forward(position_diff)
        else:
            self.backward(abs(position_diff))

    def increment(self, v: int) -> None:
        self.data[self.position] = (self.data[self.position] + v) % (self.max_value + 1)

    def decrement(self, v: int) -> None:
        self.data[self.position] = (self.data[self.position] - v) % (self.max_value + 1)

    def resetToZero(self) -> None:
        self.data[self.position] = 0

    def getValue(self) -> int:
        return self.data[self.position]

    def readInput(self) -> None:
        self.data[self.position] = ord(sys.stdin.read(1))

    def print(self, repeat_count: int = 1) -> None:
        for i in range(repeat_count):
            print(chr(self.data[self.position]), end = '')

    def printRaw(self) -> None:
        print(self.data[self.position])

    def printStructure(self) -> None:
        print('---------- Current Memory Structure ----------')
        print(f'Position: {self.position} ({self.position_dict_reversed.get(self.position, "unnamed")})')
        print(f'   Value: {self.data[self.position]}')
        print('  Memory: {', end = '')
        for key in self.position_dict:
            value: int = self.data[self.position_dict[key]]
            if (value):
                print(f"'{key}': {value}, ", end = '')
        print('}')
        print('----------------------------------------------')

#-------------------------------------#

### Command-Line Options ###

def printUsage(exit_status: int = None) -> None:
    print('''Usage
  ybrainfuck <source>.brainf

Options
  --version    #Prints the version information.
  -h,--help    #Shows this help.''')
    if (exit_status is not None):
        sys.exit(exit_status)

def printVersion() -> None:
    print(f'yBrainfuck v.{version}')

argc: int = len(sys.argv)

if (argc == 1):
    printUsage(0)
elif (argc == 2):
    if (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        printUsage(0)
    elif (sys.argv[1] == '--version'): 
        printVersion()
        sys.exit(0)
    elif (sys.argv[1].startswith('-')):
        print(f'The option [ {sys.argv[1]} ] is invalid.')
else:
    print('Only one source file can be specified.')
    print()
    printUsage(1)

#-------------------------------------#

### Read the Source ###

input_file: str = sys.argv[1]
if (not os.path.isfile(input_file)):
    print(f'The input file [ {input_file} ] does not exist.')
    sys.exit(1)

source: list = []
with open(input_file, 'r') as f:
    source = f.readlines()

variable_list: set = set()

error_flag: bool = False

for i in range(len(source)):

    line_number: int = i + 1

    source[i] = source[i].strip()

    if (source[0].startswith('[')): #ignores the first comment line if exists
        source[0] = ''

    j: int = source[i].find('#') #ignores comment lines
    if (j != -1):
        source[i] = source[i][:j]

    if (source[i].startswith('!')):
        variable_name: str = source[i][1:].strip()
        if (re.fullmatch(r'[a-zA-Z][a-zA-Z0-9_]+', variable_name)):
            if (variable_name in variable_list):
                print(f'The variable [ {variable_name} ] (line: {i}) is already defined.')
                error_flag = True
            else:
                variable_list.add(variable_name)
        else:
            print(f'The variable name [ {variable_name} ] (line: {line_number}) is invalid.')
            error_flag = True
        source[i] = ''

if (error_flag):
    sys.exit(1)

source: str = ' '.join(source) + '     ' #The appended ' ' is very useful to avoid "overrun" when parsing.

#-------------------------------------#

### Parse ###

data: BrainFuckArray = BrainFuckArray(variable_list)

iter_stack: list = []

#regex
re_alphabet:   re.Pattern = re.compile(r'[a-zA-Z]')
re_identifier: re.Pattern = re.compile(r'[a-zA-Z0-9_]')
re_digit:      re.Pattern = re.compile(r'[0-9]')

repeat_count: int = 1

iter: int = -1
len_source: int = len(source)
while (iter < len_source - 1):

    iter += 1

    c: str = source[iter] #the current character

    if (c == ' ' or c == '{' or c == '}'):
        pass
    elif (c == '~'):
        sys.exit(0)
    elif (c == '?'):
        data.printRaw()
    elif (c == '%'):
        data.printStructure()
    elif (c == '>'):
        data.forward(repeat_count)
    elif (c == '<'):
        data.backward(repeat_count)
    elif (c == '+'):
        data.increment(repeat_count)
    elif (c == '-'):
        data.decrement(repeat_count)
    elif (c == '.'):
        data.print(repeat_count)
    elif (c == ','):
        data.readInput()

    elif (c == '['):
        if (source[iter + 1] == '-' and source[iter + 2] == ']'): #Handles `[-]`, which resets the current cell to zero. Actually there is no need to handle this case specially; this is just an optimization for the speed. (Of course, `a = 0;` is much faster than `while (a) { --a; }`.)
            iter += 2
            data.resetToZero()
        else:
            if (data.getValue()):
                iter_stack.append(iter - 1)
            else:
                nest_count: int = 1
                while (True):
                    iter += 1
                    if (source[iter] == '['):
                        nest_count += 1
                    elif (source[iter] == ']'):
                        nest_count -= 1
                        if (nest_count == 0):
                            break

    elif (c == ']'):
        iter = iter_stack.pop()

    elif (re_digit.fullmatch(c)): #reads the aa under the parser and moves to the specified cell
        while (True):
            if (re_digit.fullmatch(source[iter + 1])):
                iter += 1
                c += source[iter]
            else:
                break
        repeat_count = int(c)
        continue

    elif (re_alphabet.fullmatch(c)): #reads the identifier under the parser and moves to the specified cell
        while (True):
            if (re_identifier.fullmatch(source[iter + 1])):
                iter += 1
                c += source[iter]
            else:
                break
        data.moveTo(c)

    else:
        raise Exception(f'The command [ {c} ] is invalid.')

    repeat_count = 1

