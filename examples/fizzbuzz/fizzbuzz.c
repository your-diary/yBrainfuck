#include <stdio.h>

/*-------------------------------------*/

/* Algorithm */

//Let `n` be an integer.
//1. If the current number is `3 * n`, "Fizz" shall be printed.
//   But "\n" shall not be printed since the number may also be a multiple of `5`.
//2. If the current number is `5 * n`, that is, if it ends with `0` or `5`, "Buzz\n" shall be printed.
//3. If the first condition is true but the second one is false, "\n" shall be printed.
//4. If both conditions are false, the current number shall be printed.
//   Since the range of the current number is [1..99] (`100` is not included since it's "Buzz"), we can express the current number as `10 * i + j` where the range of `i` and `j` is [0..9], which is easily printed in Brainfuck.

//By iterating over three lines at a time, we can say the first condition is always true for the third line and false for the others. For example:
//1 false
//2 false
//3 true
//4 false
//5 false
//6 true
//...

/*-------------------------------------*/

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

