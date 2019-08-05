import os
import subprocess

import pydouz


def make(src: str):
    name = os.path.basename(src)[:-3]
    pydouz.driver.make(src, f'/tmp/pydouz/{name}')
    return subprocess.call(f'/tmp/pydouz/{name}/{name}', shell=True)


def test_binop_add():
    assert make('./tests/binop_add.dz') == 4


def test_binop_div():
    assert make('./tests/binop_div.dz') == 2


def test_binop_mul():
    assert make('./tests/binop_mul.dz') == 4


def test_binop_sub():
    assert make('./tests/binop_sub.dz') == 2


def test_exit_0():
    assert make('./tests/exit_0.dz') == 0


def test_exit_1():
    assert make('./tests/exit_1.dz') == 1


def test_if_else_fib():
    assert make('./tests/if_else_fib.dz') == 89


def test_if_else():
    assert make('./tests/if_else.dz') == 1


def func_decl_call():
    assert make('./tests/func_decl_call.dz') == 3
