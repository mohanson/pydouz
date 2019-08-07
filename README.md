# The Douz Programming Language

- [Example](#Example)
- [Introduction](#Introduction)
- [Lexical elements](#Lexical-elements)
    - [Comments](#Comments)
    - [Semicolons](#Semicolons)
    - [Identifiers](#Identifiers)
    - [Keywords](#Keywords)
    - [Operators-And-Punctuation](#Operators-And-Punctuation)
    - [Operation-Notation](#Operation-Notation)
    - [Numeric](#Numeric)
    - [Block](#Block)
    - [Function-Decl](#Function-Decl)
- [Errors](#Errors)
- [Cross-Compile](#Cross-Compile)
- [Licences](#Licences)

# Example

```
$ apt install -y llvm        # Install LLVM
$ python3 setup.py develop   # Install Front End of Douz
```

```
$ cat examples/fib.dz
def fib(n) {
    if n 3 < {
        n;
    } or {
        fib(n 1 -) fib(n 2 -) +;
    };
}

def main() {
    fib(10); # Exit with code 89
}


$ python3 -m pydouz examples/fib.dz -o /tmp/fib
$ /tmp/fib/fib
$ echo $?

89
```

# Introduction

This is a reference manual for the `Douz` programming language. Douz is an experimental language for embedded and (including hardware and virtual machine design) mathematical calculation. Programs are constructed from packages.

The grammar is similar to python.

# Lexical elements

## Comments

Comments start with the character `#` and stop at the end of the line.

Sample: `# This is the simplest example: exit with code 0.`

## Semicolons

Semicolons terminate most of expression and statements.

Sample: `0;`

## Identifiers

An identifier is a sequence of one or more letters and digits. Naming of Identifiers must starts with letters.

Sample: `Alice`, `Bob02`

## Keywords

| Keyword | Description                      |
|---------|----------------------------------|
| def     | Define a function                |
| if      | Starting of conditional judgment |
| or      | The else branch for conditional  |

## Operators And Punctuation

| Operators and punctuation | Description |
|---------------------------|-------------|
| +                         | Add         |
| -                         | Sub         |
| *                         | Mul         |
| /                         | Div         |
| >                         | GT          |
| <                         | LT          |

## Operation Notation

The syntax is specified using Reverse Polish notation(RPN).

Sample: `5 1 2 + 4 * + 3 -;`, which means `5 + ((1 + 2) * 4) - 3` for human.

## Numeric

```
[ ] i8      [ ] u8
[ ] i16     [ ] u16
[ ] i32     [x] u32
[ ] i64     [ ] u64
[ ] f32     [ ] f64
```

## Block

Block starts with `{` and end with `}`. All expressions are legal in block. A block must returns a value.

Sample:
```
{
    0;
}
```

## Function Decl

Function definition starts with `def`, and then accept a block.

```
def foo()
def foo(a)
def foo(a, b)
```

# Errors

TODO

# Cross Compile

- RISCV. **First you need LLVM for riscv. Note that the LLVM provided by the Linux distribution such as Ubuntu does not include this target**. For example, the Fibonacci function, you can compile with the following code:
```
$ cat examples/riscv.py
import pydouz

driver = pydouz.driver.User(pydouz.driver.UserConf(
    llvm_config='/usr/local/llvm-riscv/bin/llvm-config',
    gcc='/usr/local/riscv/bin/riscv64-unknown-elf-gcc',
    triple='riscv64-unknown-elf',
))

driver.compile('./examples/fib.dz', '/tmp/fib')

$ python3 examples/riscv.py
```


# Licences

WTFPL
