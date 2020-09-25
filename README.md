# Introduction to Brainfuck

# 0. Index

1. [Requirement](#requirements)

2. [Syntax](#syntax)

3. [Examples](#examples)

4. [Helper Scripts](#helper-scripts)

5. [Algorithms](#algorithms)

<a id='requirements'></a>
# 1. Requirements

- To fully understand this documentation, you shall be able to write C.

<a id='syntax'></a>
# 2. Syntax

## 2.1 Comments

- Any non-reserved characters are regarded as comments.

- Any strings inside the first pair of `[` and `]` are regarded as comment. You should understand the reason for this, reading through this documentation.

## 2.2 Internal Components

In Brainfuck, there are three essential components.

| Name | Explanation |
|:-|:-|
| Data Array          | An array defined as `char data[30000] = {0};`. |
| Data Pointer        | The pointer `char *ptr = data;`. |
| Instruction Pointer | The internal parser which moves forward, parses the instructions in the source code and executes the specified command. |

Table 2.1: Internal Components in Brainfuck.

## 2.3 Reserved Characters

In Brainfuck, there are eight reserved characters.

| Character | Explanation |
|:-|:-|
| > | `++ptr;` |
| < | `--ptr;` |
| + | `++*ptr;` |
| - | `--*ptr;` |
| . | `putchar(*ptr);` |
| , | `*ptr = getchar();` |
| [ | `while (*ptr) {` |
| ] | `}` |

Table 2.2: Reserved Characters in Brainfuck.

## 2.4 References

1. [Brainfuck - Wikipedia](https://en.wikipedia.org/wiki/Brainfuck)

<a id='examples'></a>
# 3. Examples

## 3.1 Hello World

### 3.1.1 C

Here is a C version of Hello World (`./helloworld.c`) under the limitation of using only the components listed in the Table 2.2.

```C
#include <stdio.h>

char data[30000] = {0};

void print(char c) {
    static char *ptr = data;
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
```

### 3.1.2 Brainfuck

Reading the code above, you may easily understand how to port it Brainfuck. For example, to print a new line character in Brainfuck, you can just write as follows, taking into account that the ASCII character code of `\n` is `10`. Spaces are inserted just for the aesthetic purpose.
```
+++++ +++++ .>
```

So this is a Hello World in Brainfuck (`./helloworld.brainf`).
```
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>

++++++++++++++++++++++++++++++++.>

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>

+++++++++++++++++++++++++++++++++.>

++++++++++.>
```

<a id='helper-scripts'></a>
# 4. Helper Scripts

## 4.1 `bf2c.py`

`./bf2c.py` is a Python script which converts a Brainfuck source file to a C source file. Execute `./bf2c.py --help` for the usage.

For example, `./bf2c.py helloworld.brainf output.c` gives the following output. The header file `./brainfuck.h` is also included in this repository.
```C
#include <stdio.h>
#include "./brainfuck.h"

int main(void) {

    *ptr += 72;
    putchar(*ptr);
    ++ptr;
    *ptr += 101;
    putchar(*ptr);
    ++ptr;
    *ptr += 108;
    putchar(*ptr);
    ++ptr;
    *ptr += 108;
    putchar(*ptr);
    ++ptr;
    *ptr += 111;
    putchar(*ptr);
    ++ptr;
    *ptr += 32;
    putchar(*ptr);
    ++ptr;
    *ptr += 87;
    putchar(*ptr);
    ++ptr;
    *ptr += 111;
    putchar(*ptr);
    ++ptr;
    *ptr += 114;
    putchar(*ptr);
    ++ptr;
    *ptr += 108;
    putchar(*ptr);
    ++ptr;
    *ptr += 100;
    putchar(*ptr);
    ++ptr;
    *ptr += 33;
    putchar(*ptr);
    ++ptr;
    *ptr += 10;
    putchar(*ptr);
    ++ptr;

}
```

## 4.2 `brainfuck.py`

`./brainfuck.py` is an interpreter for a Brainfuck code. Internally, an input Brainfuck source `A` is transpiled to a C source `B` and `B` is compiled by `gcc` to be finally executed.

In this interpreter, we have extended Brainfuck a little for usability:

1. A number sign `#` and any text after it is ignored as a comment.

2. *Alphabetical position specifiers* are now supported. You may write `a` to jump to `data[0]`, `b` to jump to `data[1]`, ..., and `Z` to jump to `data[51]`. For example, when the current position is `data[2]`, `a+d-` is equivalent to `<<+>>>-`. Of course `<` and `>` are still supported.

3. A loop which changes the position of `ptr` is now **unsupported**. There is no warning message for it; it just doesn't work. For example, `a[>.<.]` works but `a[>.>.]` does not, because it is difficult to know how many times `>.>.` will be executed in `a[>.>.]` whilst we have to trace the current position to support the alphabetical position specifiers.

<a id='algorithms'></a>
# 5. Algorithms

In writing this section, we referred to [*Brainfuck algorithms - Esolang*](https://esolangs.org/wiki/Brainfuck_algorithms), which is published under CC0 Public Domain.

For the simplicity, hereafter we assume

- `char` is `unsigned` though the sign of `char` is implementation defined according to the C Standard.

- An identifier, which is invalid as a Brainfuck instruction and normally regarded as a comment, means "move to the cell associated with the variable of that name". For example, `a-` shall be interpreted as "move to the cell with the name `a` and decrement it".

- In a boolean expression like `x = (x == y)`, unless otherwise noted, the result is `1` when the condition is true and `0` when false.

- We sometimes add a comment of the form `# <comment>` though this is not valid in Brainfuck.

And, don't worry, we've understood and tested (if not much) all of the algorithms explained below. There is no copy-and-paste without checking its validity.

## Comments

### (a)

Since `ptr[0] == 0` at the start of an execution, we can write like this:

```bash
<start of file>[<comment>]
```

### (b)

And generally, we can write a comment after any loop since `**ptr` is always `0` just after a loop.

```bash
<loop>[<comment>]
```

### (c)

If we can accept the side effect where the current cell is cleared, this also works:

```bash
[-][<comment>]
```

## `x = 0`

```bash
x[-]
```

## `x = y`

```bash
x[-]
t[-]
y[x+t+y-] # x == y_old, t == y_old, y == 0
t[y+t-]
```

## `x += y`

```bash
t[-]
y[x+t+y-] # x == x_old + y_old, t == y_old, y == 0
t[y+t-]
```

## `x -= y`

```bash
t[-]
y[x-t+y-]
t[y+t-]
```

## `x *= y`

You may easily understand the algorithm below by thinking `x *= y` not as `x = x * y` but as `x = y * x`.

```bash
a[-]
b[-]
x[a+x-]
a[
    y[x+b+y-]
    b[y+b-]
    a-
]
```

## `x **= 2`

```bash
a[-]
b[-]
c[-]
x[a+b+x-]
a[
    b[x+c+b-]
    c[b+c-]
    a-
]
```

## `x **= y`

### (a)

You may rather want to use the algorithm (b) below.

```bash
a[-]
b[-]
c[-]
d[-]
e[-]
f[-]

# c = y - 1
y[c+d+f+y-]
d[y+d-]
c-

x[a+x-]+      # Handles `x**0 := 1` (i).

f[            # Handles `x**0 := 1` (ii).

    x-a[x+a-] # Handles `x**0 := 1` (iii).

    # e = x
    x[a+e+x-]
    a[x+a-]

    c[

        # b = x_original
        e[b+d+e-]
        d[e+d-]

        # swap(a, x)
        a[-]
        x[a+x-]

        b[
            a[x+d+a-] # x += a, d = a, a = 0
            d[a+d-]   # swap(a, d)
            b-
        ]

        c-

    ]

    f[-]

]
```

<details>
<summary>Why does this code work?</summary>

`x **= y` can be rewritten as below in Python. For example, `3**4 == 3*3*3*3 == ((3*3)*3)*3`.
```python
if (y == 0):
    x = 1
else:
    x_original: int = x
    for i in range(y - 1):
        x_current: int = x
        for j in range(x_original):
            x += x_current
```

If we reinterpret
```python
for j in range(x_original):
    x += x_current
```

as
```
for j in range(x_current):
    x += x_original
```

, we can rewrite the code as below. For example, this interprets `3**4` as `1*3*3*3*3`.
```python
x_original: int = x
x = 1
if (y):
    for i in range(y):
        x_current: int = x
        for j in range(x_current):
            x += x_original
```

This is implemented as the algorithm (b) below.

</details>

### (b)

This is much simpler.

```bash
a[-]
b[-]
c[-]
d[-]

x[a+x-] # a = x_original
x+

y[b+d+y-]
b[y+b-]

d[
    x[c+x-] # c = x_current
    c[
        a[x+b+a-] # x += x_original
        b[a+b-]
        c-
    ]
    d-
]
```

Why does this code work?: See the algorithm (a) above.

## `x /= y`

```bash
a[-]
b[-]
c[-]
d[-]
x[a+x-]
a[
    y[b+c+y-]
    c[y+c-]
    b[
        c+
        a-[c[-]d+a-]
        d[a+d-]
        c[
            b-
            [x-b[-]]+
            c-
        ]
        b-
    ]
    x+
    a
]
```

<details>
<summary>Why does this code work?</summary>

This code can be directly translated into C as below.
```cpp
unsigned char tmp;
#define swap(x, y) { tmp = x; x = y; y = tmp; }

unsigned char x = 5;
unsigned char y = 3;

int main(void) {

    unsigned char a = 0;
    unsigned char b = 0;
    unsigned char c = 0;
    unsigned char d = 0;

    if (x) {
        a = x;
        x = 0;
    }

    while (a) {
        if (y) {
            b = y;
            c = y;
            y = 0;
        }
        if (c) {
            y = c;
            c = 0;
        }
        while (b) {
            ++c;
            --a;
            while (a) {
                c = 0;
                ++d;
                --a;
            }
            if (d) {
                a = d;
                d = 0;
            }
            while (c) {
                --b;
                while (b) {
                    --x;
                    b = 0;
                }
                ++b;
                --c;
            }
            --b;
        }
        ++x;
    }

}
```

It is clear this code gives the correct result when `x == 0` or `y == 0` as far as we define `0 / 0 := 0`. So let's simplify this code with the assumption that `x != 0 && y != 0`.
```cpp
unsigned char tmp;
#define swap(x, y) { tmp = x; x = y; y = tmp; }

unsigned char x = 7;
unsigned char y = 3;

int main(void) {

    if (x == 0 || y == 0) {
        return 1;
    }

    unsigned char a = 0;
    unsigned char b = 0;

    swap(x, a);

    while (a) {
        b = y;
        while (b) {
            --a;
            if (!a) {
                --b;
                if (b) {
                    --x;
                    b = 0;
                }
                ++b;
            }
            --b;
        }
        ++x;
    }

}
```

And it is again clear this code gives the correct answer.

</details>

## `x = (x == y)`

```bash
a[-]
b[-]
x[b+x-]+ # b = x, x = 1
y[b-a+y-] # b -= y, a = y, y = 0
a[y+a-]
b[x-b[-]]
```

## `x = (x != y)`

This is almost the same as `x == (x == y)` above.

```bash
a[-]
b[-]
x[b+x-]
y[b-a+y-]
a[y+a-]
b[x+b[-]]
```

## `x = !x`

```bash
a[-]
x[a+x[-]]+
a[x-a-]
```

## `x = (x && y)`

```bash
a[-]
b[-]
x[b+x-]
b[
    [-]
    y[b+a+y-]
    a[y+a-]
    b[x+b[-]]
]
```

## `x = (x || y)`

```bash
a[-]
b[-]
c[-]
x[a+x-]
y[b+c+y-]
c[y+c-]
a[x[-]+a[-]]
b[x[-]+b[-]]
```

## `swap(x, y)`

```bash
t[-]
x[t+x-]
y[x+y-]
t[y+t-]
```

## Find A Cell of The Value `0`

Forward.

```bash
[>]
```

Backward.

```bash
[<]
```

## `while (x) { }`

```bash
x[
    {code}
    x
]
```

## `if (x) { }`

```bash
x[
    {code}
    x[-]
]
```

## `if (!x) { }`

See `if (x) { } else { }` below and make `{code1}` empty.

## `if (x) { } else { }`

```bash
a[-]
b[-]
x[a+b+x-]
a[x+a-]+
b[
    {code1}
    a-
    b[-]
]
a[
    {code2}
    a-
]
```

## TODO

- `x = (x < y)`

- `x = (x <= y)`

- `z = (x % y)`

<!-- vim: set spell nonumber: -->

