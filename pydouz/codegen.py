import typing

import llvmlite.ir

from . import ast
from . import convention
from . import error

u1 = llvmlite.ir.IntType(1)
u32 = llvmlite.ir.IntType(32)


class CodeGen:
    def __init__(self):
        self.module: llvmlite.ir.Module = llvmlite.ir.Module()
        self.ir_builder: typing.Optional[llvmlite.ir.IRBuilder] = None
        self.named_values = {}

    def text(self) -> str:
        return str(self.module)

    def save(self, path):
        with open(path, 'w') as f:
            f.write(str(self.module))

    def code_base(self, a: ast.Base):
        if isinstance(a, ast.Expression):
            return self.code_expression(a)
        if isinstance(a, ast.FunctionDefn):
            return self.code_function_defn(a)
        raise error.Error('SyntaxError')

    def code_expression(self, a: ast.Expression):
        if isinstance(a, ast.Identifier):
            return self.code_identifier(a)
        if isinstance(a, ast.Numeric):
            return self.code_numeric(a)
        if isinstance(a, ast.BinaryOperation):
            return self.code_binary_operation(a)
        if isinstance(a, ast.FunctionCall):
            return self.code_function_call(a)
        if isinstance(a, ast.If):
            return self.code_if(a)
        raise error.Error('SyntaxError')

    def code_identifier(self, a: ast.Identifier):
        return self.named_values[a.name]

    def code_numeric(self, a: ast.Numeric):
        return u32(a.n)

    def code_binary_operation(self, a: ast.BinaryOperation):
        if a.operator == convention.TOKEN_ADD:
            return self.ir_builder.add(self.code_expression(a.lhs), self.code_expression(a.rhs))
        if a.operator == convention.TOKEN_SUB:
            return self.ir_builder.sub(self.code_expression(a.lhs), self.code_expression(a.rhs))
        if a.operator == convention.TOKEN_MUL:
            return self.ir_builder.mul(self.code_expression(a.lhs), self.code_expression(a.rhs))
        if a.operator == convention.TOKEN_DIV:
            return self.ir_builder.udiv(self.code_expression(a.lhs), self.code_expression(a.rhs))
        if a.operator == convention.TOKEN_GT:
            return self.ir_builder.icmp_unsigned('>', self.code_expression(a.lhs), self.code_expression(a.rhs))
        if a.operator == convention.TOKEN_LT:
            return self.ir_builder.icmp_unsigned('<', self.code_expression(a.lhs), self.code_expression(a.rhs))
        raise error.Error('SyntaxError')

    def code_if(self, a: ast.If):
        cond = self.code_expression(a.cond)
        cond = self.ir_builder.icmp_unsigned('!=', u1(0), cond)
        with self.ir_builder.if_else(cond) as (if_then_branch, if_else_branch):
            with if_then_branch:
                if_then_block = self.ir_builder.basic_block
                if_then_out = self.code_block(a.if_then)
            with if_else_branch:
                if_else_block = self.ir_builder.basic_block
                if_else_out = self.code_block(a.if_else)
        out_phi = self.ir_builder.phi(u32)
        out_phi.add_incoming(if_then_out, if_then_block)
        out_phi.add_incoming(if_else_out, if_else_block)
        return out_phi

    def code_block(self, a: ast.Block):
        for e in a.data:
            r = self.code_base(e)
        return r

    def code_function_decl(self, a: ast.FunctionDecl):
        pass

    def code_function_defn(self, a: ast.FunctionDefn):
        func_return_type = u32
        func_args_type = [u32 for _ in a.func_decl.args]
        fnty = llvmlite.ir.FunctionType(func_return_type, func_args_type)
        func = llvmlite.ir.Function(self.module, fnty, name=a.func_decl.func_name)
        for i, e in enumerate(a.func_decl.args):
            func.args[i].name = e.name
        b = func.append_basic_block()
        self.ir_builder = llvmlite.ir.IRBuilder(b)
        for i, e in enumerate(a.func_decl.args):
            self.named_values[e.name] = func.args[i]
        r = self.code_block(a.body)
        self.ir_builder.ret(r)
        return func

    def code_function_call(self, a: ast.FunctionCall):
        func = self.module.get_global(a.func_name)
        assert isinstance(func, llvmlite.ir.values.Function)
        args = [self.code_expression(e) for e in a.args]
        return self.ir_builder.call(func, args)
