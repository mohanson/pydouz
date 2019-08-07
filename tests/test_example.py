import os
import subprocess

import pydouz


def make(path):
    b = os.path.basename(path)[:-3]
    driver = pydouz.driver.User()
    driver.compile(path, f'/tmp/pydouz/{b}')
    status, output = subprocess.getstatusoutput(f'/tmp/pydouz/{b}/{b}')
    return status, output


def test_fib():
    status, _ = make('./examples/fib.dz')
    assert status == 89
