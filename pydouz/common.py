import subprocess
import sys


def call(command):
    print(command)
    r = subprocess.call(command, shell=True)
    if r != 0:
        sys.exit(r)


class Loop:
    def __iter__(self):
        return self

    def __next__(self):
        return 0
