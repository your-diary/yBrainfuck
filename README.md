# yBrainfuck

In this repository, we introduce a new programming language called yBrainfuck. This is based on Brainfuck but a bit more human-writable. Don't worry, it's still brain-fucking. The specifications and an interpreter program for yBrainfuck are included.

Since yBrainfuck is based on Brainfuck, we first describe what is Brainfuck. If you are only interested in yBrainfuck, skip to [yBrainfuck](#ybrainfuck_spec).

Here is an example which executes `printf("d\n")`:

**Brainfuck**
```bash
> +++++ +++++    b = 10
[<++++++++++ >-] a = 100 and b = 0
<.

[-] +++++ +++++ . printf("\n");
```

**yBrainfuck**
```bash
b 10+      #b = 10
[a 10+ b-] #a = 100, b = 0
a .

[-] 10+ .  #printf("\n");
```

# 0. Index

1. [Requirement](#requirements)

2. [Syntax](#syntax)

3. [Examples](#examples)

4. [Helper Scripts](#helper_scripts)

5. [yBrainfuck](#ybrainfuck_spec)

6. [Algorithms](#algorithms)

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
| Data Array          | An array defined as `char data[30000] = {0};`. We say `data` consists of `30000` *cells*. |
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

1. [*Brainfuck - Wikipedia*](https://en.wikipedia.org/wiki/Brainfuck)

<a id='examples'></a>
# 3. Examples

## 3.1 Hello World

### 3.1.1 C

Here is a C version of Hello World (`./examples/helloworld/helloworld.c`) under the limitation of using only the components listed in the Table 2.2.

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

Reading the code above, you may easily understand how to port it to Brainfuck. For example, to print a new line character in Brainfuck, you can just write as follows, taking into account that the ASCII character code of `\n` is `10`. Spaces are inserted just for the aesthetic purpose.
```
+++++ +++++ .
```

So this is a Hello World in Brainfuck (`./examples/helloworld/helloworld.brainf`).
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

## 3.2 FizzBuzz

### 3.2.1 Python

If you don't know [the FizzBuzz game](https://en.wikipedia.org/wiki/Fizz_buzz), don't worry. You may instantly understand the rule by reading this simple implementation (`./examples/fizzbuzz/fizzbuzz.py`).
```python
for i in range(1, 101):
    if ((i % 3 == 0) and (i % 5 == 0)):
        print('FizzBuzz')
    elif (i % 3 == 0):
        print('Fizz')
    elif (i % 5 == 0):
        print('Buzz')
    else:
        print(i)
```

Here is the output (`./examples/fizzbuzz/correct_output.txt`).
```
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
16
17
Fizz
19
Buzz
Fizz
22
23
Fizz
Buzz
26
Fizz
28
29
FizzBuzz
31
32
Fizz
34
Buzz
Fizz
37
38
Fizz
Buzz
41
Fizz
43
44
FizzBuzz
46
47
Fizz
49
Buzz
Fizz
52
53
Fizz
Buzz
56
Fizz
58
59
FizzBuzz
61
62
Fizz
64
Buzz
Fizz
67
68
Fizz
Buzz
71
Fizz
73
74
FizzBuzz
76
77
Fizz
79
Buzz
Fizz
82
83
Fizz
Buzz
86
Fizz
88
89
FizzBuzz
91
92
Fizz
94
Buzz
Fizz
97
98
Fizz
Buzz
```

### 3.2.2 C

The C implementation below (`./examples/fizzbuzz/fizzbuzz.c`) is written in somewhat an eccentric way but this is totally intentional. See the comments (omitted in the code below) in the file for the algorithm.
```cpp
#include <stdio.h>

int main(void) {

    unsigned char t = 0;
    unsigned char u = 10;
    while (u) {
        t += 10;
        --u;
    }

    unsigned char i = 0;
    unsigned char j = 0;

    const unsigned char a = 0;
    const unsigned char b = 5;
    const unsigned char c = 9;
    unsigned char d = 0;
    unsigned char e = 0;
    unsigned char f = 0;

    while (t) {

        //#1
        {
            //#a
            d = (j == c);
            if (d) {
                ++i;
                j = 0;
            } else {
                ++j;
            }

            //#b
            d = (j == a);
            e = (j == b);
            f = (d || e);
            if (f) {
                printf("Buzz\n");
            } else {
                if (i) {
                    printf("%d", i);
                }
                printf("%d\n", j);
            }

            --t;
        }

        if (t) {

            //This is exactly the same as #1.
            {
                d = (j == c);
                if (d) {
                    ++i;
                    j = 0;
                } else {
                    ++j;
                }

                d = (j == a);
                e = (j == b);
                f = (d || e);
                if (f) {
                    printf("Buzz\n");
                } else {
                    if (i) {
                        printf("%d", i);
                    }
                    printf("%d\n", j);
                }
                --t;
            }

            //#2
            {
                //This is exactly the same as #a.
                d = (j == c);
                if (d) {
                    ++i;
                    j = 0;
                } else {
                    ++j;
                }

                //#c
                printf("Fizz");
                d = (j == a);
                e = (j == b);
                f = (d || e);
                if (f) {
                    printf("Buzz");
                }
                printf("\n");

                --t;
            }

        }

    }

}
```

### 3.2.3 Brainfuck

Just by copying and pasting the algorithms described in [Algorithms](#algorithms), we can directly translate the C code above to a Brainfuck code. For the simplicity, we use yBrainfuck 2.0 instead of Brainfuck. Here is the code (`./examples/fizzbuzz/fizzbuzz_v2.brainf`):
```bash
#declarations {

!iter

i #second digit of the current number
j #first digit of that

#const
a
b
c

#tmp
d
e
f

#tmp
p
q
r
s
t
u
v

#tmp
U
V

#} declarations

#iter = 100
#p used but reset to zero
iter[-]
p[-]
p 10+
[
    iter 10+
    p -
]

b[-]
c[-]
b 5+
c 9+

iter[
    #1
    {
        #a
        {
            #d = j
            #q used but reset to zero
            d[-]
            p[-]
            j[d+ p+ j-]
            p[j+ p-]

            #d = (j == c)
            #p, q used but reset to zero
            p[-]
            q[-]
            d[q+d-]+
            c[q-p+c-]
            p[c+p-]
            q[d-q[-]]

            #if (d) { } else { }
            #p, q used but reset to zero
            p[-]
            q[-]
            d[p+q+d-]
            p[d+p-]+
            q[
                {
                    i +
                    j[-]
                }
                p-
                q[-]
            ]
            p[
                {
                    j +
                }
                p-
            ]

            d[-] #all tmps reset to zero
        }

        #b
        {
            #b' {

            #d, e = j
            #q used but reset to zero
            d[-]
            e[-]
            p[-]
            j[d+ e+ p+ j-]
            p[j+ p-]

            #d = (j == a)
            #p, q used but reset to zero
            p[-]
            q[-]
            d[q+d-]+
            a[q-p+a-]
            p[a+p-]
            q[d-q[-]]

            #e = (j == b)
            #p, q used but reset to zero
            p[-]
            q[-]
            e[q+e-]+
            b[q-p+b-]
            p[b+p-]
            q[e-q[-]]

            #d = (d || e)
            #f reset to zero
            p[-]
            q[-]
            r[-]
            d[p+d-]
            e[q+r+e-]
            r[e+r-]
            p[d[-]+p[-]]
            q[d[-]+q[-]]
            f[-]

            #} b'

            #if (d) { } else { }
            #p, q, r used but reset to zero
            p[-]
            q[-]
            d[p+q+d-]
            p[d+p-]+
            q[
                {
                    #printf("Buzz\n")
                    #r used but reset to zero
                    r[-]
                    66+ . [-]
                    117+ . [-]
                    122+ . . [-]
                    10+ . [-]
                }
                p-
                q[-]
            ]
            p[
                {
                    #if (i) { }
                    #s, t, u, v used but reset to zero
                    s[-]
                    t[-]
                    u[-]
                    v[-]
                    i[s+ t+ i-]
                    t[i+ t-]
                    s[
                        #printf("%d", i)
                        {
                            i[u+ v+ i-]
                            v[i+ v-]
                            u 48+ . [-]
                        }
                        s[-]
                    ]
                    #print(j + '\n')
                    j[u+ v+ j-]
                    v[j+ v-]
                    u 48+ . [-]
                    u 10+ . [-]
                }
                p-
            ]
        }

        iter -
    }

    #if (iter) { }
    #U, V used but reset to zero
    iter[U+ V+ iter-]
    V[iter+ V-]
    U[
        #This is exactly the same as #1.
        {
            #a
            {
                #d = j
                #q used but reset to zero
                d[-]
                p[-]
                j[d+ p+ j-]
                p[j+ p-]

                #d = (j == c)
                #p, q used but reset to zero
                p[-]
                q[-]
                d[q+d-]+
                c[q-p+c-]
                p[c+p-]
                q[d-q[-]]

                #if (d) { } else { }
                #p, q used but reset to zero
                p[-]
                q[-]
                d[p+q+d-]
                p[d+p-]+
                q[
                    {
                        i +
                        j[-]
                    }
                    p-
                    q[-]
                ]
                p[
                    {
                        j +
                    }
                    p-
                ]

                d[-] #all tmps reset to zero
            }

            #b
            {
                #d, e = j
                #q used but reset to zero
                d[-]
                e[-]
                p[-]
                j[d+ e+ p+ j-]
                p[j+ p-]

                #d = (j == a)
                #p, q used but reset to zero
                p[-]
                q[-]
                d[q+d-]+
                a[q-p+a-]
                p[a+p-]
                q[d-q[-]]

                #e = (j == b)
                #p, q used but reset to zero
                p[-]
                q[-]
                e[q+e-]+
                b[q-p+b-]
                p[b+p-]
                q[e-q[-]]

                #d = (d || e)
                #f reset to zero
                p[-]
                q[-]
                r[-]
                d[p+d-]
                e[q+r+e-]
                r[e+r-]
                p[d[-]+p[-]]
                q[d[-]+q[-]]
                f[-]

                #if (d) { } else { }
                #p, q, r used but reset to zero
                p[-]
                q[-]
                d[p+q+d-]
                p[d+p-]+
                q[
                    #x
                    {
                        #printf("Buzz\n")
                        #r used but reset to zero
                        r[-]
                        66+ . [-]
                        117+ . [-]
                        122+ . . [-]
                        10+ . [-]
                    }
                    p-
                    q[-]
                ]
                p[
                    {
                        #if (i) { }
                        #s, t, u, v used but reset to zero
                        s[-]
                        t[-]
                        u[-]
                        v[-]
                        i[s+ t+ i-]
                        t[i+ t-]
                        s[
                            #printf("%d", i)
                            {
                                i[u+ v+ i-]
                                v[i+ v-]
                                u 48+ . [-]
                            }
                            s[-]
                        ]
                        #print(j + '\n')
                        j[u+ v+ j-]
                        v[j+ v-]
                        u 48+ . [-]
                        u 10+ . [-]
                    }
                    p-
                ]
            }

            iter -
        }

        #2
        {
            #This is exactly the same as #a.
            {
                #d = j
                #q used but reset to zero
                d[-]
                p[-]
                j[d+ p+ j-]
                p[j+ p-]

                #d = (j == c)
                #p, q used but reset to zero
                p[-]
                q[-]
                d[q+d-]+
                c[q-p+c-]
                p[c+p-]
                q[d-q[-]]

                #if (d) { } else { }
                #p, q used but reset to zero
                p[-]
                q[-]
                d[p+q+d-]
                p[d+p-]+
                q[
                    {
                        i +
                        j[-]
                    }
                    p-
                    q[-]
                ]
                p[
                    {
                        j +
                    }
                    p-
                ]

                d[-] #all tmps reset to zero
            }

            #c
            {
                #printf("Fizz")
                #r used but reset to zero
                r[-]
                70+ . [-]
                105+ . [-]
                122+ . . [-]

                #{
                #This is exactly the same as #b'

                #d, e = j
                #q used but reset to zero
                d[-]
                e[-]
                p[-]
                j[d+ e+ p+ j-]
                p[j+ p-]

                #d = (j == a)
                #p, q used but reset to zero
                p[-]
                q[-]
                d[q+d-]+
                a[q-p+a-]
                p[a+p-]
                q[d-q[-]]

                #e = (j == b)
                #p, q used but reset to zero
                p[-]
                q[-]
                e[q+e-]+
                b[q-p+b-]
                p[b+p-]
                q[e-q[-]]

                #d = (d || e)
                #f reset to zero
                p[-]
                q[-]
                r[-]
                d[p+d-]
                e[q+r+e-]
                r[e+r-]
                p[d[-]+p[-]]
                q[d[-]+q[-]]
                f[-]

                #}

                #if (d) { }
                #p, q used but reset to zero
                p[-]
                q[-]
                d[p+ q+ d-]
                q[d+ q-]
                p[
                    #This is almost the same as #x
                    #The only difference is "\n" is not output here.
                    {
                        #printf("Buzz")
                        #r used but reset to zero
                        r[-]
                        66+ . [-]
                        117+ . [-]
                        122+ . . [-]
                    }
                    p[-]
                ]

                #printf("\n")
                #r used but reset to zero
                r[-]
                10+ . [-]

            }

            iter -
        }

        U[-]
    ]

    iter

]
```

<a id='helper_scripts'></a>
# 4. Helper Scripts

## 4.1 `brainfuck.py`

`./brainfuck.py` is a transpiler from Brainfuck to C. Execute `./brainfuck.py --help` for the usage.

For example, `./brainfuck.py helloworld.brainf output.c` gives the following output. The header file `./brainfuck.h` is also included in this repository.
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

### Known Bugs

- [Asymmetric Loops](#asymmetric_loops) is not supported.

## 4.2 `ybrainfuck_v1.py`

`./ybrainfuck_v1.py` is an interpreter for a yBrainfuck 1.x code. Internally, an input yBrainfuck source `A` is transpiled to a C source `B` and `B` is compiled by `gcc` to be finally executed.

### Known Bugs

<a id='asymmetric_loops'></a>
#### Asymmetric Loops

A loop which doesn't revert the position change of `ptr` is not supported. There is no warning message for it; it just doesn't work. For example, the code below doesn't work.
```bash
a +
b ++

a[b-a->] #This loop starts with `a` but each iteration ends with `b`.

c ++++++++++++++++++++++++++++++++++++++++++++++++ . [-]
  ++++++++++ .

#Expected result: printf("0\n");
```

This bug is easily fixed but neglected for the time being. We are free from this bug in `ybrainfuck_v2.py`.

## 4.3 `ybrainfuck_v2.py`

`./ybrainfuck_v2.py` is an interpreter for a yBrainfuck 2.x code. This is really an interpreter; the C code is no longer generated.

## 4.4 `ybrainfuck_v2.js`

`./browser_version/ybrainfuck_v2/ybrainfuck_v2.js` is a yBrainfuck interpreter which is ported from `./ybrainfuck_v2.py` and works in any browsers. You can open `./browser_version/ybrainfuck_v2/index.html` or just access our [webpage](https://your-diary.com/apps/ybrainfuck/index.html) to try it.

<a id='ybrainfuck_spec'></a>
# 5. yBrainfuck

## 5.1 About

In this section, we introduce a new language *yBrainfuck*, which is similar to Brainfuck but a bit more human-writable. Currently, yBrainfuck 1.x and yBrainfuck 2.x are available.

## 5.2 Compilers / Interpreters

See [Helper Scripts](#helper_scripts) for the interpreters we supply. The easiest way to execute a yBrainfuck code is to use [the browser version](https://your-diary.com/apps/ybrainfuck/index.html).

## 5.3 Specifications

yBrainfuck is based on Brainfuck. The extensions listed below have been made.

| Syntax | Explanation | Examples | First Available Version |
|:-|:-|:-|:-|
| | | |
| | `unsigned char` is used for the array `data` while in Brainfuck `char` is used. Since the sign of `char` is implementation defined in C, we decided instead to use `unsigned char` to remove the ambiguity. The range of each cell (i.e. `data[i]`) is `[0..255]` and, as defined in the C Standard, overflows never occur; `255 + 1 == 0` and `0 - 1 == 255`. | | 1.0 |
| `#<text>` | This is ignored as a comment. You may write this style of comment at the middle of a line. | `a[-] #resets to zero` | 1.0 |
| `<alphabet>` | *Alphabetical position specifiers*. You may write `a` to jump to `data[0]`, `b` to jump to `data[1]`, ..., and `Z` to jump to `data[51]`. For example, when the current position is `data[2]`, `a+d-` is equivalent to `<<+>>>-`. | `a+`, `a[b-a->]` | 1.0 |
| | | |
| | Accessing a memory location out of the reserved cells is not permissive. Such buffer overruns are detected, terminating the program right away as a result. In Brainfuck, they are not detected and invokes undefined behaviors. | `a<` (NG), `b<` (OK) | 2.0 |
| ` `, `{`, `}` | As in Brainfuck, these characters are still ignored. Since yBrainfuck 2.x, the other non-command characters not inside a comment are forbidden. | `>[-] (^_^)` (NG), `>[-] #(^_^)` (OK) | 2.0 |
| `!<identifier>` | This names a cell and makes `<identifier>` usable as an alphabetical position specifier. An *identifier* is defined as `[a-zA-Z][a-zA-Z0-9_]+`. Spaces may be inserted between `!` and `<identifier>`. For example, if you write `!tmp1` and `!tmp2`, now `data[52]` and `data[53]` (**not** necessarily respectively<sup>†1</sup>) can also be accessed via those names. | `!iter`, `! iter` | 2.0 |
| `<number><command>` | This repeats `<command>` for `<number>` times. Spaces shall not be inserted between `<number>` and `<command>`. The supported commands are `>`, `<`, `+`, `-` and `.`. For example, `3+` is interpreted as `+++`. | `a [-] 10+ .` | 2.0 |
| `?` | This prints the value of the current cell as an integer. This is equivalent to `printf("%d\n", **ptr);` in C. This may be useful for debugging purposes. | `?` | 2.0 |
| `%` | This prints the current position, its value and the list of cells with non-zero values. This may be useful for debugging purposes. | `%` | 2.0 |
| `~` | This terminates the program right away. This is equivalent to `exit(0)` in C. | `~` | 2.0 |

†1: The order of allocations is randomly and dynamically determined since all of the variable definitions are first read and stored in an unordered set in the initialization step, which is entered before the allocation step. Generally, when you define `n` variables in total in your source code, `data[52]`, ..., `data[52+n-1]` are available with those names but which name will be associated with which cell is undefined.

<a id='algorithms'></a>
# 6. Algorithms

In this section we describe some essential algorithms used in Brainfuck (not specific to yBrainfuck). In writing this section, we referred to [*Brainfuck algorithms - Esolang*](https://esolangs.org/wiki/Brainfuck_algorithms), which is published under CC0 Public Domain.

For the simplicity, hereafter we assume

- `char` is `unsigned` though the sign of `char` is implementation defined according to the C Standard.

- An identifier, which is invalid as a Brainfuck instruction and normally regarded as a comment, means "move to the cell associated with the name". For example, `a-` shall be interpreted as "move to the cell with the name `a` and decrement it".

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

This is why the algorithm (a) above works.

Now, if we reinterpret
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

Side Effect: `x` is cleared.

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

