import argparse
import ctypes
import sys

from . import codegen
from . import driver
from . import parser
from . import tokenization


def parse():
    p = argparse.ArgumentParser()
    p_sub = p.add_subparsers(help='sub commands', dest='cmd')
    p_build = p_sub.add_parser('build', help='compile packages and dependencies')
    p_build.add_argument('src')
    p_build.add_argument('-o')
    p_run = p_sub.add_parser('run', help='compile and run Douz program')
    p_run.add_argument('src')
    p_run.add_argument('-o')

    args = p.parse_args()

    if args.cmd == 'build':
        d = driver.User()
        d.compile(args.src, args.o)
        return

    if args.cmd == 'run':
        with open(args.src, 'r') as f:
            t = tokenization.Tokenization(f)
            p = parser.Parser(t)
            c = codegen.CodeGen()
            for e in p.iter():
                c.code_base(e)
            llvm_ir = c.text()

        d = driver.Lite()
        d.compile_ir(llvm_ir)

        func_ptr = d.engine.get_function_address('main')
        cfunc = ctypes.CFUNCTYPE(ctypes.c_uint)(func_ptr)
        status = cfunc()
        print(f'Exit: {status}')
        sys.exit(status)
        return

    p.print_help()
