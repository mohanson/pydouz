import typing

from . import convention


class Base:
    pass


class Expression(Base):
    pass


class Statement(Base):
    pass


class Identifier(Expression):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'Ast.Identifier<name={self.name}>'


class Numeric(Expression):
    def __init__(self, n: int):
        self.n = n

    def __repr__(self):
        return f'Ast.Numeric<n={self.n}>'


class BinaryOperation(Expression):
    def __init__(self, operator: int, lhs: Base, rhs: Base):
        self.operator = operator
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        op = {
            convention.TOKEN_ADD: convention.KEYWORDS_ADD,
            convention.TOKEN_SUB: convention.KEYWORDS_SUB,
            convention.TOKEN_MUL: convention.KEYWORDS_MUL,
            convention.TOKEN_DIV: convention.KEYWORDS_DIV,
            convention.TOKEN_GT: convention.KEYWORDS_GT,
            convention.TOKEN_LT: convention.KEYWORDS_LT,
        }[self.operator]
        return f'Ast.BinaryOperation<operator={op}, lhs={self.lhs}, rhs={self.rhs}>'


class Block(Base):
    def __init__(self, data: typing.List[Base]):
        self.data = data

    def __repr__(self):
        return f'Ast.Block<data={self.data}>'


class If(Expression):
    def __init__(self, cond: Expression, if_then: Block, if_else: Block):
        self.cond = cond
        self.if_then = if_then
        self.if_else = if_else

    def __repr__(self):
        return f'Ast.If<cond={self.cond}, then={self.if_then}, else={self.if_else}>'


class Let(Statement):
    def __init__(self, identifier: Identifier, expression: Expression):
        self.identifier = identifier
        self.expression = expression

    def __repr__(self):
        return f'Ast.Let<identifier={self.identifier}, expression={self.expression}>'


class Ptr(Statement):
    def __init__(self, identifier: Identifier, expression: Expression):
        self.identifier = identifier
        self.expression = expression

    def __repr__(self):
        return f'Ast.Ptr<identifier={self.identifier}, expression={self.expression}>'


class For(Statement):
    def __init__(self, cond: Expression, body: Block):
        self.cond = cond
        self.body = body

    def __repr__(self):
        return f'Ast.For<cond={self.cond}, body={self.body}>'


class FunctionDecl(Base):
    def __init__(self, func_name: str, args: typing.List[Identifier]):
        self.func_name = func_name
        self.args = args

    def __repr__(self):
        return f'Ast.FunctionDecl<func_name={self.func_name}, args={self.args}>'


class FunctionDefn(Base):
    def __init__(self, func_decl: FunctionDecl, body: Base):
        self.func_decl = func_decl
        self.body = body

    def __repr__(self):
        return f'Ast.FunctionDefn<func_decl={self.func_decl}, body={self.body}>'


class FunctionCall(Expression):
    def __init__(self, func_name: str, args: typing.List[Base]):
        self.func_name = func_name
        self.args = args

    def __repr__(self):
        return f'Ast.FunctionCall<func_name={self.func_name} args={self.args}>'
