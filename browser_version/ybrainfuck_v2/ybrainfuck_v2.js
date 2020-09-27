//An interpreter for yBrainfuck 2.x.
//This is ported from "../ybrainfuck_v2.py" of the version 2.0.1.

(function() {
    "use strict";

    /*-------------------------------------*/

    /* Event */

    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey == true && e.key == 'Enter') { //Ctrl+Enter
            e.preventDefault();
            console.log('execute(): Executing...');
            execute();
            console.log('execute(): Done.');
        }
    });

    document.querySelector('#run_button').addEventListener('click', (e) => {
        console.log('execute(): Executing...');
        execute();
        console.log('execute(): Done.');
    });

    document.querySelector('#reset_button').addEventListener('click', (e) => {
        result_area.innerHTML = '';
        document.querySelector('#source_area').value = '';
    });

    window.addEventListener('load', (e) => {
        document.querySelector('#source_area').value = window.localStorage.getItem('source_code');
        document.querySelector('#stdin_area').value = window.localStorage.getItem('stdin');
    });

    window.addEventListener('unload', (e) => {
        window.localStorage.setItem('source_code', document.querySelector('#source_area').value);
        window.localStorage.setItem('stdin', document.querySelector('#stdin_area').value);
    });

    /*-------------------------------------*/

    /* Result Area */

    /* object */ const result_area = document.querySelector('#result_area');
    /* bool */ let error_flag = false;

    function print(/* str */ s = '') /* -> undefined */ {
        s = s.replace(/\n/g, '<br>');
        result_area.innerHTML += s;
    }

    function print_error(/* str */ s = '') /* -> undefined */ {
        error_flag = true;
        print(`<br><span style='color: Red;'>${s}</span>`);
    }

    /*-------------------------------------*/

    /* Classes */

    class BrainFuckArray {

        constructor(/* set */ variable_list) /* -> undefined */ {
            
            /* bool */ this.error_flag = false;

            /* str */ this.stdin = document.querySelector('#stdin_area').value;
            /* int */ this.stdin_index = 0;

            /* unsigned char */ this.min_value = 0;
            /* unsigned char */ this.max_value = 255;

            /* int */ this.min_position = 0;
            /* int */ this.max_position = 30000 - 1;

            /* array */ this.data = new Array(this.max_position - this.min_position + 1).fill(0);

            /* int */ this.position = 0;
            /* map */ this.position_dict = new Map();
            /* map */ this.position_dict_reversed = new Map(); //for `this.printStructure()`

            /* str */ let builtin_variables = 'abcdefghijklmnopqrstuvwxyz' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

            for (let i = 0; i < builtin_variables.length; ++i) {
                let char = builtin_variables[i];
                this.position_dict.set(char, i);
                this.position_dict_reversed.set(i, char);
            }

            let i = this.position_dict.size;
            for (let variable_name of variable_list) {
                this.position_dict.set(variable_name, i);
                this.position_dict_reversed.set(i, variable_name);
                ++i;
            }

        }

        forward(/* int */ num_shift = 1) /* -> undefined */ {
            this.position += num_shift;
            if (this.position > this.max_position) {
                print_error(`Buffer overrun occurred. The current position [ ${this.position} ] exceeds \`${this.max_position}\`.\n`);
            }
        }

        backward(/* int */ num_shift = 1) /* -> undefined */ {
            this.position -= num_shift;
            if (this.position < this.min_position) {
                print_error(`Buffer overrun occurred. The current position has the negative value [ ${this.position} ].\n`);
            }
        }

        moveTo(/* str */ variable_name) /* -> undefined */ {
            if (!this.position_dict.has(variable_name)) {
                print_error(`The variable [ ${variable_name} ] is not defined.\n`);
                return;
            }
            /* int */ let position_diff = this.position_dict.get(variable_name) - this.position;
            if (position_diff > 0) {
                this.forward(position_diff);
            } else {
                this.backward(Math.abs(position_diff));
            }
        }

        increment(/* int */ v) /* -> undefined */ {
            this.data[this.position] += v % (this.max_value + 1);
            if (this.data[this.position] > this.max_value) {
                this.data[this.position] -= (this.max_value + 1);
            }
        }

        decrement(/* int */ v) /* -> undefined */ {
            this.data[this.position] -= v % (this.max_value + 1);
            if (this.data[this.position] < 0) {
                this.data[this.position] += (this.max_value + 1);
            }
        }

        resetToZero() /* -> undefined */ {
            this.data[this.position] = 0;
        }

        getValue() /* -> int */ {
            return this.data[this.position];
        }

        readInput() /* -> undefined */ {
            if (this.stdin_index >= this.stdin.length) {
                print_error('The [ , ] command is specified while EOF is already reached.\n');
                return;
            }
            this.data[this.position] = this.stdin.charCodeAt(this.stdin_index);
            ++this.stdin_index;
        }

        print(repeat_count = 1) /* -> undefined */ {
            for (let i = 0; i < repeat_count; ++i) {
                print(String.fromCharCode(this.data[this.position]));
            }
        }

        printRaw() /* -> undefined */ {
            print(this.data[this.position] + '\n');
        }

        printStructure() /* -> undefined */ {
            print('---------- Current Memory Structure ----------\n');
            print(`Position: ${this.position} (${this.position_dict_reversed.get(this.position) == undefined ? "unnamed" : this.position_dict_reversed.get(this.position)})\n`);
            print(`   Value: ${this.data[this.position]}\n`);
            print('  Memory: {');
            for (let l of this.position_dict) {
                let cell_name  = l[0];
                let cell_index = l[1];
                let cell_value = this.data[cell_index];
                if (cell_value) {
                    print(`'${cell_name}': ${cell_value}, `);
                }
            }
            print('}\n');
            print('----------------------------------------------\n');
        }

    }

    /*-------------------------------------*/

    /* main */

    function execute() {

        error_flag = false;
        result_area.innerHTML = '';

        /*-------------------------------------*/

        /* Reads the Source */

        /* array */ let source = document.querySelector('#source_area').value.split('\n');

        let variable_list = new Set();

        for (let i = 0; i < source.length; ++i) {

            let line_number = i + 1;

            source[i] = source[i].trim();

            //ignores comment lines
            /* int */ let j = source[i].indexOf('#');
            if (j != -1) {
                source[i] = source[i].slice(0, j);
            }

            if (source[i].startsWith('!')) {
                let variable_name = source[i].slice(1).trim();
                if (variable_name.match(/^[a-zA-Z][a-zA-Z0-9_]+$/)) {
                    if (variable_list.has(variable_name)) {
                        print_error(`The variable [ ${variable_name} ] (line: ${line_number}) is already defined.\n`);
                    } else {
                        variable_list.add(variable_name);
                    }
                } else {
                    print_error(`The variable name [ ${variable_name} ] (line: ${line_number}) is invalid.\n`);
                }
                source[i] = '';
            }

        }

        if (error_flag) {
            return;
        }

        /* str */ source = source.join(' ') + '     '; //The appended ' ' is very useful to avoid "overrun" when parsing.

        /*-------------------------------------*/

        /* Parse */

        /* BrainFuckArray */ let data = new BrainFuckArray(variable_list);

        let iter_stack = [];

        //regex
        const re_alphabet   = /[a-zA-Z]/;
        const re_identifier = /[a-zA-Z0-9_]/;
        const re_digit      = /[0-9]/;

        let repeat_count = 1;

        let iter = -1;
        const len_source = source.length;
        while (iter < len_source - 1) {

            ++iter;

            let c = source[iter]; //the current character

            if (c == ' ' || c == '{' || c == '}') {
                ;
            } else if (c == '~') {
                return;
            } else if (c == '?') {
                data.printRaw();
            } else if (c == '%') {
                data.printStructure();
            } else if (c == '>') {
                data.forward(repeat_count);
            } else if (c == '<') {
                data.backward(repeat_count);
            } else if (c == '+') {
                data.increment(repeat_count);
            } else if (c == '-') {
                data.decrement(repeat_count);
            } else if (c == '.') {
                data.print(repeat_count);
            } else if (c == ',') {
                data.readInput();
            } else if (c == '[') {
                if (source[iter + 1] == '-' && source[iter + 2] == ']') { //Handles `[-]`, which resets the current cell to zero. Actually there is no need to handle this case specially; this is just an optimization for the speed. (Of course, `a = 0;` is much faster than `while (a) { --a; }`.)
                    iter += 2;
                    data.resetToZero();
                } else {
                    if (data.getValue()) {
                        iter_stack.push(iter - 1);
                    } else {
                        let nest_count = 1;
                        while (true) {
                            ++iter;
                            if (source[iter] == '[') {
                                ++nest_count;
                            } else if (source[iter] == ']') {
                                --nest_count;
                                if (nest_count == 0) {
                                    break;
                                }
                            }
                        }
                    }
                }

            } else if (c == ']') {
                iter = iter_stack.pop();

            } else if (c.match(re_digit)) { //reads the number under the parser and stores it as `repeat_count`
                while (true) {
                    if (source[iter + 1].match(re_digit)) {
                        ++iter;
                        c += source[iter];
                    } else {
                        break;
                    }
                }
                repeat_count = Number.parseInt(c);
                continue;

            } else if (c.match(re_alphabet)) { //reads the identifier under the parser and moves to the specified cell
                while (true) {
                    if (source[iter + 1].match(re_identifier)) {
                        ++iter;
                        c += source[iter];
                    } else {
                        break;
                    }
                }
                data.moveTo(c);

            } else {
                print_error(`The command [ ${c} ] is invalid.\n`);
            }

            repeat_count = 1;

            if (error_flag) {
                return;
            }

        }

        /*-------------------------------------*/

        print('<span style="color: #777777;">EOF</span>');

    }

    /*-------------------------------------*/

})();

