import ctypes
import io
import textwrap

import pydouz


def make(code):
    t = pydouz.tokenization.Tokenization(io.StringIO(code))
    p = pydouz.parser.Parser(t)
    c = pydouz.codegen.CodeGen()
    for e in p.iter():
        c.code_base(e)
    llvm_ir = c.text()
    print(llvm_ir)

    driver = pydouz.driver.Lite()
    driver.compile_ir(llvm_ir)
    return driver.engine


def test_exit_0():
    engine = make(textwrap.dedent('''
    def main() {
        0;
    }
    '''))
    func_ptr = engine.get_function_address('main')
    cfunc = ctypes.CFUNCTYPE(ctypes.c_uint)(func_ptr)
    assert cfunc() == 0


def test_exit_1():
    engine = make(textwrap.dedent('''
    def main() {
        1;
    }
    '''))
    func_ptr = engine.get_function_address('main')
    cfunc = ctypes.CFUNCTYPE(ctypes.c_uint)(func_ptr)
    assert cfunc() == 1


def test_if():
    engine = make(textwrap.dedent('''
    def main(n) {
        if n 11 > {
            1;
        } or {
            0;
        };
    }
    '''))
    func_ptr = engine.get_function_address('main')
    cfunc = ctypes.CFUNCTYPE(ctypes.c_uint, ctypes.c_uint)(func_ptr)
    assert cfunc(12) == 1
    assert cfunc(11) == 0
    assert cfunc(10) == 0


def test_fib():
    engine = make(textwrap.dedent('''
    def fib(n) {
        if n 3 < {
            n;
        } or {
            fib(n 1 -) fib(n 2 -) +;
        };
    }
    '''))
    func_ptr = engine.get_function_address('fib')
    cfunc = ctypes.CFUNCTYPE(ctypes.c_uint, ctypes.c_uint)(func_ptr)
    assert cfunc(10) == 89
    assert cfunc(9) == 55


def test_let():
    engine = make(textwrap.dedent('''
    def main(n) {
        let a = n;
        let a = a 1 +;
        let b = a;
        b;
    }
    '''))
    func_ptr = engine.get_function_address('main')
    cfunc = ctypes.CFUNCTYPE(ctypes.c_uint, ctypes.c_uint)(func_ptr)
    assert cfunc(1) == 2
    assert cfunc(2) == 3


def test_for():
    engine = make(textwrap.dedent('''
    def sum(n) {
        ptr i = 0;
        ptr s = 0;
        for i n <; {
            ptr s = s i +;
            ptr i = i 1 +;
        };
        s;
    }
    '''))
    func_ptr = engine.get_function_address('sum')
    cfunc = ctypes.CFUNCTYPE(ctypes.c_uint, ctypes.c_uint)(func_ptr)
    assert cfunc(4) == 6
    assert cfunc(5) == 10
    assert cfunc(6) == 15
