# pydouz

pydouz is a toy language with LLVM backend.

```
$ apt install llvm          # Install LLVM
$ python3 setup.py develop  # Install pydouz
```

# Example

```
$ cat examples/sample.dz
def foo(a, b):
    a b + 10 *

def main():
    foo(1, 2)

$ python3 pydouz_main.py examples/sample.dz -o /tmp/sample.ll
$ lli /tmp/sample.ll
$ echo $?

30
```

# Licences

WTFPL
