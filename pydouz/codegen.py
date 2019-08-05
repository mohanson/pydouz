import llvmlite.binding
import llvmlite.ir

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

    def code_number(self, asti: ast.Number):
        return llvmlite.ir.IntType(32)(int(asti.n))

    def code_var(self, asti: ast.Var):
        return self.locals[asti.name]

    def code_if(self, asti: ast.If):
        cond = self.code(asti.cond)
        cond = self.ir_builder.icmp_unsigned('!=', llvmlite.ir.IntType(1)(0), cond)
        with self.ir_builder.if_else(cond) as (if_then_branch, if_else_branch):
            with if_then_branch:
                if_then_block = self.ir_builder.basic_block
                if_then_out = self.code(asti.if_then)
            with if_else_branch:
                if_else_block = self.ir_builder.basic_block
                if_else_out = self.code(asti.if_else)

        out_phi = self.ir_builder.phi(llvmlite.ir.IntType(32))
        out_phi.add_incoming(if_then_out, if_then_block)
        out_phi.add_incoming(if_else_out, if_else_block)

        return out_phi

    def code_binop(self, asti: ast.Binop):
        if asti.operator == convention.TOKEN_ADD:
            return self.ir_builder.add(self.code(asti.lhs), self.code(asti.rhs))
        if asti.operator == convention.TOKEN_SUB:
            return self.ir_builder.sub(self.code(asti.lhs), self.code(asti.rhs))
        if asti.operator == convention.TOKEN_MUL:
            return self.ir_builder.mul(self.code(asti.lhs), self.code(asti.rhs))
        if asti.operator == convention.TOKEN_DIV:
            return self.ir_builder.udiv(self.code(asti.lhs), self.code(asti.rhs))
        if asti.operator == convention.TOKEN_GT:
            return self.ir_builder.icmp_unsigned('>', self.code(asti.lhs), self.code(asti.rhs))
        if asti.operator == convention.TOKEN_LT:
            return self.ir_builder.icmp_unsigned('<', self.code(asti.lhs), self.code(asti.rhs))
        raise ''

    def code_func_defn(self, asti: ast.FunctionDefn):
        func_return = llvmlite.ir.IntType(32)
        func_args = [llvmlite.ir.IntType(32) for _ in asti.func_decl.args]
        fnty = llvmlite.ir.FunctionType(func_return, func_args)
        func = llvmlite.ir.Function(self.module, fnty, name=asti.func_decl.func_name)

        self.functions[asti.func_decl.func_name] = len(self.functions)

        block = func.append_basic_block()
        self.ir_builder = llvmlite.ir.IRBuilder(block)

        for i, e in enumerate(asti.func_decl.args):
            self.locals[e.name] = func.args[i]
        r = self.code(asti.func_body)
        self.ir_builder.ret(r)

        return func

    def code_func_call(self, asti: ast.FunctionCall):
        func = self.module.functions[self.functions[asti.func_name]]
        args = [self.code(e) for e in asti.args]
        return self.ir_builder.call(func, args)

    def code(self, asti):
        if isinstance(asti, ast.Number):
            return self.code_number(asti)
        if isinstance(asti, ast.Var):
            return self.code_var(asti)
        if isinstance(asti, ast.If):
            return self.code_if(asti)
        if isinstance(asti, ast.Binop):
            return self.code_binop(asti)
        if isinstance(asti, ast.FunctionDefn):
            return self.code_func_defn(asti)
        if isinstance(asti, ast.FunctionCall):
            return self.code_func_call(asti)
        raise ''
