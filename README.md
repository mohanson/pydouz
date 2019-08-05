# The Douz Programming Language

- [Introduction](#Introduction)
- [Lexical elements](#Lexical-elements)
- [Example](#Example)

# Introduction

This is a reference manual for the `Douz` programming language. Douz is an experimental language for embedded and (including hardware and virtual machine design) mathematical calculation. Programs are constructed from packages.

The grammar is similar to python.

# Lexical elements

TODO

# Example

```
$ apt install llvm          # Install LLVM
$ python3 setup.py develop  # Install pydouz
```

```
$ cat tests/if_else_fib.dz
def fib(n):
    if n 3 <:
        n
    or:
        fib(n 1 -) fib(n 2 -) +

def main():
    fib(10)

$ python3 pydouz_main.py tests/if_else_fib.dz -o /tmp/if_else_fib.ll
$ lli /tmp/if_else_fib.ll
$ echo $?

89
```

# Licences

WTFPL
