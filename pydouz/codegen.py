import llvmlite.ir
import llvmlite.binding

from . import ast
from . import convention

llvmlite.binding.initialize()
llvmlite.binding.initialize_native_target()
llvmlite.binding.initialize_native_asmprinter()

class CodeGen:

    def __init__(self):
        self.module = llvmlite.ir.Module()
        self.module.triple = llvmlite.binding.get_default_triple()
        self.ir_builder: llvmlite.ir.IRBuilder = None

        self.locals = {}
        self.functions = {}

    def save(self, path):
        with open(path, 'w') as f:
            f.write(str(self.module))

    def code_var(self, asti: ast.Var):
        return self.locals[asti.name]

    def code_number(self, asti: ast.Number):
        return llvmlite.ir.IntType(32)(int(asti.n))

    def code_binop(self, asti: ast.Binop):
        if asti.operator == convention.TOKEN_ADD:
            return self.ir_builder.add(self.code(asti.lhs), self.code(asti.rhs))
        if asti.operator == convention.TOKEN_SUB:
            return self.ir_builder.sub(self.code(asti.lhs), self.code(asti.rhs))
        if asti.operator == convention.TOKEN_MUL:
            return self.ir_builder.mul(self.code(asti.lhs), self.code(asti.rhs))
        if asti.operator == convention.TOKEN_DIV:
            return self.ir_builder.div(self.code(asti.lhs), self.code(asti.rhs))
        raise ''

    def code_func_defn(self, asti: ast.FunctionDefn):
        func_return = llvmlite.ir.IntType(32)
        func_args = [llvmlite.ir.IntType(32) for _ in asti.func_decl.args]
        fnty = llvmlite.ir.FunctionType(func_return, func_args)
        func = llvmlite.ir.Function(self.module, fnty, name=asti.func_decl.func_name)

        block = func.append_basic_block()
        self.ir_builder = llvmlite.ir.IRBuilder(block)

        for i, e in enumerate(asti.func_decl.args):
            self.locals[e.name] = func.args[i]
        r = self.code(asti.func_body)
        self.ir_builder.ret(r)

        self.functions[asti.func_decl.func_name] = len(self.functions)

        return func

    def code_func_call(self, asti: ast.FunctionCall):
        func = self.module.functions[self.functions[asti.func_name]]
        args = [self.code(e) for e in asti.args]
        return self.ir_builder.call(func, args)

    def code(self, asti):
        if isinstance(asti, ast.Var):
            return self.code_var(asti)
        if isinstance(asti, ast.Number):
            return self.code_number(asti)
        if isinstance(asti, ast.Binop):
            return self.code_binop(asti)
        if isinstance(asti, ast.FunctionDefn):
            return self.code_func_defn(asti)
        if isinstance(asti, ast.FunctionCall):
            return self.code_func_call(asti)
        raise ''
