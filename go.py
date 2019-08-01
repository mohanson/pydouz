import subprocess
import sys


def call(command):
    print(command)
    r = subprocess.call(command, shell=True)
    if r != 0:
        sys.exit(r)


def main():
    call(f'py pydouz_main.py examples/sample.dz -o /tmp/sample.ll')


if __name__ == '__main__':
    main()
