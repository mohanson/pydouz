import os
import subprocess

import llvmlite.binding

from . import codegen
from . import common
from . import parser
from . import tokenization


class Lite:
    llvmlite.binding.initialize()
    llvmlite.binding.initialize_native_target()
    llvmlite.binding.initialize_native_asmprinter()

    def __init__(self):
        # Create a target machine representing the host
        target = llvmlite.binding.Target.from_default_triple()
        target_machine = target.create_target_machine()
        # And an execution engine with an empty backing module
        backing_mod = llvmlite.binding.parse_assembly('')
        self.engine = llvmlite.binding.create_mcjit_compiler(backing_mod, target_machine)

    def compile_ir(self, llvm_ir):
        # Create a LLVM module object from the IR
        mod = llvmlite.binding.parse_assembly(llvm_ir)
        mod.verify()
        # Now add the module and make sure it is ready for execution
        self.engine.add_module(mod)
        self.engine.finalize_object()
        self.engine.run_static_constructors()
        return mod


class UserConf:
    def __init__(self, llvm_config=None, gcc=None, triple=None):
        self.llvm_config = llvm_config or 'llvm-config'
        self.llvm_prefix = subprocess.getoutput(f'{self.llvm_config} --prefix')
        self.gcc = gcc or 'gcc'
        self.triple = triple or llvmlite.binding.get_default_triple()


class User:
    def __init__(self, conf=None):
        self.conf = conf or UserConf()

    def compile(self, code_dz, save):
        os.makedirs(save, 0o644, exist_ok=True)
        with open(code_dz, 'r') as f:
            t = tokenization.Tokenization(f)
            p = parser.Parser(t)
            c = codegen.CodeGen()
            c.module.triple = self.conf.triple
            for e in p.iter():
                c.code_base(e)

        b = os.path.basename(save)
        p_ll = os.path.join(save, b + '.ll')
        p_bc = os.path.join(save, b + '.bc')
        p_s = os.path.join(save, b + '.s')
        p_o = os.path.join(save, b)
        # LLVM IR
        c.save(p_ll)
        # LLVM ByteCode
        common.call(f'{self.conf.llvm_prefix}/bin/llvm-as {p_ll} -o {p_bc}')
        # LLVM Assemble
        common.call(f'{self.conf.llvm_prefix}/bin/llc {p_bc} -o {p_s}')
        # GCC
        common.call(f'{self.conf.gcc} {p_s} -o {p_o}')
