from . import convention


class Var:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'ast.var<name = {self.name}>'


class Number:
    def __init__(self, n):
        self.n = n

    def __repr__(self):
        return f'ast.number<n = {self.n}>'


class Binop:
    def __init__(self, operator, lhs, rhs):
        self.operator = operator
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        op = {
            convention.TOKEN_ADD: convention.KEYWORDS_ADD,
            convention.TOKEN_SUB: convention.KEYWORDS_SUB,
            convention.TOKEN_MUL: convention.KEYWORDS_MUL,
            convention.TOKEN_DIV: convention.KEYWORDS_DIV,
        }[self.operator]
        return f'ast.binop<operator={op}, lhs={self.lhs}, rhs={self.rhs}>'


class FunctionDecl:
    def __init__(self, func_name, args):
        self.func_name = func_name
        self.args = args

    def __repr__(self):
        args = '[' + ', '.join([str(e) for e in self.args]) + ']'
        return f'ast.function_decl<func_name = {self.func_name} args = {args}>'


class FunctionDefn:
    def __init__(self, func_decl: FunctionDecl, func_body):
        self.func_decl = func_decl
        self.func_body = func_body

    def __repr__(self):
        return f'ast.function_defn<func_decl = {self.func_decl}, func_body = {self.func_body}>'


class FunctionCall:
    def __init__(self, func_name, args):
        self.func_name = func_name
        self.args = args

    def __repr__(self):
        return f'ast.function_call<func_name = {self.func_name} args = [{", ".join([str(e) for e in self.args])}]>'
