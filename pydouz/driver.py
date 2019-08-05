import os
import os.path
import subprocess
import sys

from . import codegen
from . import convention
from . import parser
from . import tokenization


def call(command):
    print(command)
    r = subprocess.call(command, shell=True)
    if r != 0:
        sys.exit(r)


def make(src: str, dst: str):
    os.makedirs(dst, 0o644, exist_ok=True)
    fname = os.path.basename(src)[:-3]

    dst_ll = os.path.join(dst, fname + '.ll')
    dst_bc = os.path.join(dst, fname + '.bc')
    dst_o = os.path.join(dst, fname + '.o')
    dst_b = os.path.join(dst, fname)

    # LLVM IR
    with open(src) as f:
        c = codegen.CodeGen()
        a = tokenization.Tokenization(f)
        p = parser.Parser(a)
        for e in p.parse():
            c.code(e)

        c.save(dst_ll)

    # LLVM ByteCode
    call(f'{convention.GLOBAL_LLVM_AS} {dst_ll} -o {dst_bc}')

    # LLVM Obj
    call(f'{convention.GLOBAL_LLC} -filetype=obj {dst_bc}')

    # GCC
    call(f'{convention.GLOBAL_GCC} {dst_o} -o {dst_b}')
