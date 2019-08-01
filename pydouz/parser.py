from . import common
from . import ast
from . import convention
from . import token
from . import tokenization


class Parser:
    def __init__(self, tokenization: tokenization.Tokenization):
        self.tokenization = tokenization
        self.t: token.Token = self.tokenization.next()
        self.s = []

    def parse_identifier(self):
        name = self.t.s
        self.t = self.tokenization.next()
        if self.t.kind != convention.TOKEN_L_PARAN:
            return ast.Var(name)

        args = []
        self.t = self.tokenization.next()
        for _ in common.Long():
            if self.t.kind == convention.TOKEN_R_PARAN:
                self.t = self.tokenization.next()
                break
            if self.t.kind == convention.TOKEN_IDENTIFIER:
                t = self.parse_identifier()
                args.append(t)
                continue
            if self.t.kind == convention.TOKEN_NUMBER:
                t = self.parse_number()
                args.append(t)
                continue

        return ast.FunctionCall(name, args)

    def parse_number(self):
        n = self.t.s
        self.t = self.tokenization.next()
        return ast.Number(n)

    def parse_expression(self, lhs):
        if self.t.kind == convention.TOKEN_EOL:
            return lhs

        rhs = self.parse_val()
        op = self.t.kind
        self.t = self.tokenization.next()

        return self.parse_expression(ast.Binop(op, lhs, rhs))

    def parse_func_decl(self):
        self.t = self.tokenization.next()
        if self.t.kind != convention.TOKEN_IDENTIFIER:
            raise ''

        func_name = self.t.s
        self.t = self.tokenization.next()
        if self.t.kind != convention.TOKEN_L_PARAN:
            raise ''

        args = []
        self.t = self.tokenization.next()
        for _ in common.Long():
            if self.t.kind == convention.TOKEN_IDENTIFIER:
                t = self.parse_identifier()
                args.append(t)
                continue
            if self.t.kind == convention.TOKEN_R_PARAN:
                self.t = self.tokenization.next()
                break

        if self.t.kind != convention.TOKEN_COLON:
            raise ''
        self.t = self.tokenization.next()

        if self.t.kind != convention.TOKEN_EOL:
            raise ''
        self.t = self.tokenization.next()

        return ast.FunctionDecl(func_name, args)

    def parse_func_defn(self):
        func_decl = self.parse_func_decl()
        func_body = self.parse_expression(self.parse_val())
        return ast.FunctionDefn(func_decl, func_body)

    def parse_val(self):
        # Identifier or Number
        if self.t.kind == convention.TOKEN_NUMBER:
            return self.parse_number()
        return self.parse_identifier()

    def parse(self):
        r = []
        for _ in common.Long():

            for _ in common.Long():
                if self.t.kind == convention.TOKEN_EOL:
                    self.t = self.tokenization.next()
                    continue
                break

            if self.t.kind == convention.TOKEN_EOF:
                break

            a = self.parse_func_defn()
            r.append(a)

        return r
