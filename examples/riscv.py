import pydouz

driver = pydouz.driver.User(pydouz.driver.UserConf(
    llvm_config='/usr/local/llvm-riscv/bin/llvm-config',
    gcc='/usr/local/riscv/bin/riscv64-unknown-elf-gcc',
    triple='riscv64-unknown-elf',
))

driver.compile('./examples/fib.dz', '/tmp/fib')
