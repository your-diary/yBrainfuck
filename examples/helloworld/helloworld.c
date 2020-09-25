#include <stdio.h>
#include "./brainfuck.h"

void print(char c) {
    *ptr += c;
    putchar(*ptr);
    ++ptr;
}

int main(void) {

    print('H');
    print('e');
    print('l');
    print('l');
    print('o');
    print(' ');
    print('W');
    print('o');
    print('r');
    print('l');
    print('d');
    print('!');
    print('\n');

}

