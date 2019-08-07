from . import ast
from . import common
from . import convention
from . import token


class Parser:
    def __init__(self, tokenization):
        self.tokenization = tokenization
        self.t: token.Token = self.tokenization.next()

    def parse_expr_number(self):
        n = self.t.s
        self.t = self.tokenization.next()
        return ast.Number(n)

    def parse_expr_identifier(self):
        name = self.t.s
        self.t = self.tokenization.next()
        if self.t.kind != convention.TOKEN_L_PARAN:
            return ast.Var(name)
        # Parse function call
        args = []
        self.t = self.tokenization.next()
        for _ in common.Long():
            # )
            if self.t.kind == convention.TOKEN_R_PARAN:
                self.t = self.tokenization.next()
                break
            # ,
            if self.t.kind == convention.TOKEN_COMMA:
                self.t = self.tokenization.next()
                continue
            # Expr
            t = self.parse_expr()
            args.append(t)

        return ast.FunctionCall(name, args)

    def parse_expr_if(self):
        self.t = self.tokenization.next()
        # Condition
        cond = self.parse_expr()
        assert self.t.kind == convention.TOKEN_COLON
        self.t = self.tokenization.next()
        assert self.t.kind == convention.TOKEN_EOL
        self.t = self.tokenization.next()
        # Then expression
        self.t = self.tokenization.next()
        if_then = self.parse_expr()
        assert self.t.kind == convention.TOKEN_EOL
        self.t = self.tokenization.next()
        # Else
        self.t = self.tokenization.next()
        assert self.t.kind == convention.TOKEN_ELSE
        self.t = self.tokenization.next()
        assert self.t.kind == convention.TOKEN_COLON
        self.t = self.tokenization.next()
        assert self.t.kind == convention.TOKEN_EOL
        self.t = self.tokenization.next()
        # Else expression
        self.t = self.tokenization.next()
        if_else = self.parse_expr()
        return ast.If(cond, if_then, if_else)

    def parse_expr_base(self):
        if self.t.kind == convention.TOKEN_NUMBER:
            return self.parse_expr_number()
        if self.t.kind == convention.TOKEN_IDENTIFIER:
            return self.parse_expr_identifier()
        if self.t.kind == convention.TOKEN_IF:
            return self.parse_expr_if()
        raise ''

    def parse_expr_binop(self, lhs=None):
        # LHS
        if not lhs:
            lhs = self.parse_expr()
        if self.t.kind in [
            convention.TOKEN_EOL,
            convention.TOKEN_COLON,
            convention.TOKEN_R_PARAN,
        ]:
            return lhs
        # RHS
        rhs = self.parse_expr()
        # OP
        op = self.t.kind
        self.t = self.tokenization.next()
        return self.parse_expr_binop(ast.Binop(op, lhs, rhs))

    def parse_expr(self):
        lhs = self.parse_expr_base()
        if self.t.kind in [
            convention.TOKEN_ADD,
            convention.TOKEN_SUB,
            convention.TOKEN_MUL,
            convention.TOKEN_DIV,
            convention.TOKEN_GT,
            convention.TOKEN_LT,
            convention.TOKEN_COMMA,
            convention.TOKEN_R_PARAN,
            convention.TOKEN_EOL,
        ]:
            return lhs
        return self.parse_expr_binop(lhs)

    def parse_func_decl(self):
        self.t = self.tokenization.next()
        # Parse function name
        assert self.t.kind == convention.TOKEN_IDENTIFIER
        func_name = self.t.s
        # Parse (
        self.t = self.tokenization.next()
        assert self.t.kind == convention.TOKEN_L_PARAN
        # Parse arguments
        args = []
        self.t = self.tokenization.next()
        for _ in common.Long():
            # Arg
            if self.t.kind == convention.TOKEN_IDENTIFIER:
                t = self.parse_expr_base()
                assert isinstance(t, ast.Var)
                args.append(t)
                continue
            # ,
            if self.t.kind == convention.TOKEN_COMMA:
                self.t = self.tokenization.next()
                assert self.tokenization.back(1).kind == convention.TOKEN_IDENTIFIER
                continue
            # )
            if self.t.kind == convention.TOKEN_R_PARAN:
                self.t = self.tokenization.next()
                break
        # Parse :
        assert self.t.kind == convention.TOKEN_COLON
        self.t = self.tokenization.next()
        # Parse EOL
        assert self.t.kind == convention.TOKEN_EOL
        self.t = self.tokenization.next()

        return ast.FunctionDecl(func_name, args)

    def parse_func_defn(self):
        func_decl = self.parse_func_decl()
        assert self.t.kind == convention.TOKEN_SPACE
        self.t = self.tokenization.next()
        func_body = self.parse_expr()
        return ast.FunctionDefn(func_decl, func_body)

    def parse(self):
        r = []
        for _ in common.Long():
            if self.t.kind == convention.TOKEN_EOF:
                break
            if self.t.kind == convention.TOKEN_EOL:
                self.t = self.tokenization.next()
                continue
            a = self.parse_func_defn()
            r.append(a)

        return r
