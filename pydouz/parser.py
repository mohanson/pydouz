import typing

from . import ast
from . import common
from . import convention
from . import error
from . import tokenization

_ = tokenization.Tokenization


class Parser:
    def __init__(self, tokenization: tokenization.Tokenization):
        self.tokenization = tokenization
        self.t: tokenization.Token = self.tokenization.next()
        self.stack: typing.List[ast.Expression] = []

    def parse_identifier(self) -> ast.Identifier:
        name = self.t.s
        self.t = self.tokenization.next()
        if self.t.kind != convention.TOKEN_L_S_PAREN:
            return ast.Identifier(name)
        # Parse function call
        args = []
        self.t = self.tokenization.next()
        for _ in common.Loop():
            # )
            if self.t.kind == convention.TOKEN_R_S_PAREN:
                self.t = self.tokenization.next()
                break
            # ,
            if self.t.kind == convention.TOKEN_COMMA:
                self.t = self.tokenization.next()
                continue
            # Expr
            t = self.parse_expression()
            args.append(t)

        return ast.FunctionCall(name, args)

    def parse_numeric(self) -> ast.Numeric:
        a = ast.Numeric(int(self.t.s))
        self.t = self.tokenization.next()
        return a

    def parse_binary_operation(self) -> ast.BinaryOperation:
        rhs = self.stack.pop()
        lhs = self.stack.pop()
        r = ast.BinaryOperation(self.t.kind, lhs, rhs)
        self.t = self.tokenization.next()
        return r

    def parse_if(self):
        self.t = self.tokenization.next()
        # Condition
        cond = self.parse_expression()
        # Then
        if_then = self.parse_block()
        # Else Keyword
        self.t = self.tokenization.next()
        # Else
        if_else = self.parse_block()
        return ast.If(cond, if_then, if_else)

    def parse_expression(self) -> ast.Expression:
        for _ in common.Loop():
            if self.t.kind == convention.TOKEN_NUMERIC:
                a = self.parse_numeric()
                self.stack.append(a)
            if self.t.kind == convention.TOKEN_IDENTIFIER:
                a = self.parse_identifier()
                self.stack.append(a)
            if self.t.kind == convention.TOKEN_IF:
                a = self.parse_if()
                self.stack.append(a)
            if self.t.kind in [
                convention.TOKEN_ADD,
                convention.TOKEN_SUB,
                convention.TOKEN_MUL,
                convention.TOKEN_DIV,
                convention.TOKEN_GT,
                convention.TOKEN_LT,
            ]:
                a = self.parse_binary_operation()
                self.stack.append(a)
            if self.t.kind in [
                convention.TOKEN_L_L_PAREN,
                convention.TOKEN_R_S_PAREN,
                convention.TOKEN_COMMA,
                convention.TOKEN_SEMICOLON,
            ]:
                return self.stack.pop()
        raise error.Error('SyntaxError')

    def parse_let(self) -> ast.Let:
        self.t = self.tokenization.next()
        # Identifier
        identifier = self.parse_identifier()
        # =
        if self.t.kind != convention.TOKEN_EQUAL:
            raise error.Error('SyntaxError')
        # Expression
        self.t = self.tokenization.next()
        expression = self.parse_expression()
        return ast.Let(identifier, expression)

    def parse_ptr(self) -> ast.Ptr:
        self.t = self.tokenization.next()
        # Identifier
        identifier = self.parse_identifier()
        # =
        if self.t.kind != convention.TOKEN_EQUAL:
            raise error.Error('SyntaxError')
        # Expression
        self.t = self.tokenization.next()
        expression = self.parse_expression()
        return ast.Ptr(identifier, expression)

    def parse_for(self) -> ast.For:
        self.t = self.tokenization.next()
        # Condition
        cond = self.parse_expression()
        # ;
        if self.t.kind != convention.TOKEN_SEMICOLON:
            raise error.Error('SyntaxError')
        self.t = self.tokenization.next()
        # Body
        body = self.parse_block()
        return ast.For(cond, body)

    def parse_statement(self) -> ast.Statement:
        if self.t.kind == convention.TOKEN_LET:
            return self.parse_let()
        if self.t.kind == convention.TOKEN_FOR:
            return self.parse_for()
        if self.t.kind == convention.TOKEN_PTR:
            return self.parse_ptr()
        raise error.Error('SyntaxError')

    def parse_block(self) -> ast.Block:
        self.t = self.tokenization.next()
        b = []
        for _ in common.Loop():
            # }
            if self.t.kind == convention.TOKEN_R_L_PAREN:
                self.t = self.tokenization.next()
                break
            # Statement or Expression
            e = self.next()
            b.append(e)
            # ;
            if self.t.kind != convention.TOKEN_SEMICOLON:
                raise error.Error('SyntaxError')
            self.t = self.tokenization.next()
            continue
        return ast.Block(b)

    def parse_func_decl(self):
        self.t = self.tokenization.next()
        # Parse function name
        assert self.t.kind == convention.TOKEN_IDENTIFIER
        func_name = self.t.s
        # Parse (
        self.t = self.tokenization.next()
        assert self.t.kind == convention.TOKEN_L_S_PAREN
        # Parse arguments
        args = []
        self.t = self.tokenization.next()
        for _ in common.Loop():
            # )
            if self.t.kind == convention.TOKEN_R_S_PAREN:
                self.t = self.tokenization.next()
                break
            # ,
            if self.t.kind == convention.TOKEN_COMMA:
                self.t = self.tokenization.next()
                continue
            # Expr
            t = self.parse_identifier()
            args.append(t)

        return ast.FunctionDecl(func_name, args)

    def parse_func_defn(self):
        func_decl = self.parse_func_decl()
        body = self.parse_block()
        return ast.FunctionDefn(func_decl, body)

    def iter(self):
        for _ in common.Loop():
            r = self.next()
            if not r:
                break
            yield r

    def next(self) -> ast.Base:
        return self.take()

    def take(self) -> ast.Base:
        if self.t.kind in [
            convention.TOKEN_IDENTIFIER,
            convention.TOKEN_NUMERIC,
        ]:
            return self.parse_expression()
        if self.t.kind in [
            convention.TOKEN_LET,
            convention.TOKEN_PTR,
            convention.TOKEN_FOR,
        ]:
            return self.parse_statement()
        if self.t.kind == convention.TOKEN_L_L_PAREN:
            return self.parse_block()
        if self.t.kind == convention.TOKEN_DEF:
            return self.parse_func_defn()
        if self.t.kind == convention.TOKEN_IF:
            return self.parse_if()
        if self.t.kind == convention.TOKEN_EOF:
            return None
        raise error.Error('SyntaxError')
