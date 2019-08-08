# The Douz Programming Language

![img](./res/douz.jpg)

# Installation

```
$ apt install -y llvm        # Install LLVM
$ pip3 install pydouz        # Install Front End of Douz
```

# Play

Pydouz is a compiled language, but it comes with a JIT interpreter at the same time, so you can "run" source code directly:

```
$ pydouz run ./examples/fib.dz
Exit: 89
```

Or you can compile it to a executable output:

```
$ pydouz build ./examples/fib.dz -o /tmp/fib
```

# Licences

WTFPL
