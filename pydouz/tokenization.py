import typing

from . import common
from . import convention
from . import error


class Token:
    def __init__(self, kind: int, s: str):
        self.kind = kind
        self.s = s

    def __repr__(self):
        if self.kind == convention.TOKEN_EOF:
            return f'Token.EOF'
        if self.kind == convention.TOKEN_EOL:
            return f'Token.EOL'
        if self.kind == convention.TOKEN_SPACE:
            return f'Token.Space({len(self.s)})'
        if self.kind == convention.TOKEN_NUMERIC:
            return f'Token.Numeric({self.s})'
        if self.kind == convention.TOKEN_COMMENT:
            return f'Token.Comment({self.s})'
        if self.kind == convention.TOKEN_L_S_PAREN:
            return f'Token.{convention.KEYWORDS_L_S_PAREN}'
        if self.kind == convention.TOKEN_R_S_PAREN:
            return f'Token.{convention.KEYWORDS_R_S_PAREN}'
        if self.kind == convention.TOKEN_L_M_PAREN:
            return f'Token.{convention.KEYWORDS_L_M_PAREN}'
        if self.kind == convention.TOKEN_R_M_PAREN:
            return f'Token.{convention.KEYWORDS_R_M_PAREN}'
        if self.kind == convention.TOKEN_L_L_PAREN:
            return f'Token.{convention.KEYWORDS_L_L_PAREN}'
        if self.kind == convention.TOKEN_R_L_PAREN:
            return f'Token.{convention.KEYWORDS_R_L_PAREN}'
        if self.kind == convention.TOKEN_ADD:
            return f'Token.{convention.KEYWORDS_ADD}'
        if self.kind == convention.TOKEN_SUB:
            return f'Token.{convention.KEYWORDS_SUB}'
        if self.kind == convention.TOKEN_MUL:
            return f'Token.{convention.KEYWORDS_MUL}'
        if self.kind == convention.TOKEN_DIV:
            return f'Token.{convention.KEYWORDS_DIV}'
        if self.kind == convention.TOKEN_GT:
            return f'Token.{convention.KEYWORDS_GT}'
        if self.kind == convention.TOKEN_LT:
            return f'Token.{convention.KEYWORDS_LT}'
        if self.kind == convention.TOKEN_EQUAL:
            return f'Token.{convention.KEYWORDS_EQUAL}{convention.KEYWORDS_EQUAL}'
        if self.kind == convention.TOKEN_COMMA:
            return f'Token.{convention.KEYWORDS_COMMA}'
        if self.kind == convention.TOKEN_COLON:
            return f'Token.{convention.KEYWORDS_COLON}'
        if self.kind == convention.TOKEN_SEMICOLON:
            return f'Token.{convention.KEYWORDS_SEMICOLON}'
        if self.kind == convention.TOKEN_IDENTIFIER:
            return f'Token.Identifier({self.s})'
        if self.kind == convention.TOKEN_DEF:
            return f'Token.Def'
        if self.kind == convention.TOKEN_IF:
            return f'Token.If'
        if self.kind == convention.TOKEN_ELSE:
            return f'Token.Else'
        if self.kind == convention.TOKEN_LET:
            return f'Token.Let'
        if self.kind == convention.TOKEN_PTR:
            return f'Token.Ptr'
        if self.kind == convention.TOKEN_FOR:
            return f'Token.For'
        raise error.Error('')


class Tokenization:
    def __init__(self, reader: typing.TextIO):
        self.reader = reader
        self.c = ''

    def iter(self):
        r = self.next()
        yield r
        if r.kind == convention.TOKEN_EOF:
            return
        yield from self.iter()

    def next(self) -> Token:
        t = self.take()
        if t.kind in [
            convention.TOKEN_EOL,
            convention.TOKEN_SPACE,
            convention.TOKEN_COMMENT,
        ]:
            return self.next()
        return t

    def take(self) -> Token:
        if not self.c:
            self.c = self.reader.read(1)

        # EOF
        if not self.c:
            return Token(convention.TOKEN_EOF, '')

        # EOL
        if self.c == convention.KEYWORDS_EOL:
            self.c = self.reader.read(1)
            return Token(convention.TOKEN_EOL, convention.KEYWORDS_EOL)

        s = ''

        # SPACE
        if self.c == convention.KEYWORDS_SPACE:
            s += self.c
            for _ in common.Loop():
                self.c = self.reader.read(1)
                if self.c == convention.KEYWORDS_SPACE:
                    s += self.c
                    continue
                break
            return Token(convention.TOKEN_SPACE, s)

        # Identifier && keywords
        if self.c.isalpha():
            s += self.c
            for _ in common.Loop():
                self.c = self.reader.read(1)
                if self.c.isalnum():
                    s += self.c
                    continue
                break

            # Def
            if s == convention.KEYWORDS_DEF:
                return Token(convention.TOKEN_DEF, convention.KEYWORDS_DEF)
            # If
            if s == convention.KEYWORDS_IF:
                return Token(convention.TOKEN_IF, s)
            # Else
            if s == convention.KEYWORDS_ELSE:
                return Token(convention.TOKEN_ELSE, s)
            # Let
            if s == convention.KEYWORDS_LET:
                return Token(convention.TOKEN_LET, s)
            # Ptr
            if s == convention.KEYWORDS_PTR:
                return Token(convention.TOKEN_PTR, s)
            # For
            if s == convention.KEYWORDS_FOR:
                return Token(convention.TOKEN_FOR, s)
            return Token(convention.TOKEN_IDENTIFIER, s)

        # Number
        if self.c.isdigit():
            s += self.c
            self.c = self.reader.read(1)
            for _ in common.Loop():
                if self.c.isalnum():
                    s += self.c
                    self.c = self.reader.read(1)
                    continue
                break
            if s.startswith('0x'):
                return Token(convention.TOKEN_NUMERIC, int(s, 16))
            return Token(convention.TOKEN_NUMERIC, int(s))

        # Comment
        if self.c == convention.KEYWORDS_COMMENT:
            for _ in common.Loop():
                self.c = self.reader.read(1)
                if self.c == convention.KEYWORDS_EOL:
                    break
                s += self.c
                continue
            return Token(convention.TOKEN_COMMENT, s)

        # L_S_Paren:
        if self.c == convention.KEYWORDS_L_S_PAREN:
            self.c = self.reader.read(1)
            return Token(convention.TOKEN_L_S_PAREN, convention.KEYWORDS_L_S_PAREN)

        # R_S_Paren:
        if self.c == convention.KEYWORDS_R_S_PAREN:
            self.c = self.reader.read(1)
            return Token(convention.TOKEN_R_S_PAREN, convention.KEYWORDS_R_S_PAREN)

        # L_M_Paren:
        if self.c == convention.KEYWORDS_L_M_PAREN:
            self.c = self.reader.read(1)
            return Token(convention.TOKEN_L_M_PAREN, convention.KEYWORDS_L_M_PAREN)

        # R_M_Paren:
        if self.c == convention.KEYWORDS_R_M_PAREN:
            self.c = self.reader.read(1)
            return Token(convention.TOKEN_R_M_PAREN, convention.KEYWORDS_R_M_PAREN)

        # L_L_Paren:
        if self.c == convention.KEYWORDS_L_L_PAREN:
            self.c = self.reader.read(1)
            return Token(convention.TOKEN_L_L_PAREN, convention.KEYWORDS_L_L_PAREN)

        # R_S_Paren:
        if self.c == convention.KEYWORDS_R_L_PAREN:
            self.c = self.reader.read(1)
            return Token(convention.TOKEN_R_L_PAREN, convention.KEYWORDS_R_L_PAREN)

        # Add
        if self.c == convention.KEYWORDS_ADD:
            self.c = self.reader.read(1)
            return Token(convention.TOKEN_ADD, convention.KEYWORDS_ADD)

        # Sub
        if self.c == convention.KEYWORDS_SUB:
            self.c = self.reader.read(1)
            return Token(convention.TOKEN_SUB, convention.KEYWORDS_SUB)

        # Mul
        if self.c == convention.KEYWORDS_MUL:
            self.c = self.reader.read(1)
            return Token(convention.TOKEN_MUL, convention.KEYWORDS_MUL)

        # Div
        if self.c == convention.KEYWORDS_DIV:
            self.c = self.reader.read(1)
            return Token(convention.TOKEN_DIV, convention.KEYWORDS_DIV)

        # Comma
        if self.c == convention.KEYWORDS_COMMA:
            self.c = self.reader.read(1)
            return Token(convention.TOKEN_COMMA, convention.KEYWORDS_COMMA)

        # Colon
        if self.c == convention.KEYWORDS_COLON:
            self.c = self.reader.read(1)
            return Token(convention.TOKEN_COLON, convention.KEYWORDS_COLON)

        # SEMICOLON
        if self.c == convention.KEYWORDS_SEMICOLON:
            self.c = self.reader.read(1)
            return Token(convention.TOKEN_SEMICOLON, convention.KEYWORDS_SEMICOLON)

        # GT
        if self.c == convention.KEYWORDS_GT:
            self.c = self.reader.read(1)
            return Token(convention.TOKEN_GT, convention.KEYWORDS_GT)

        # LT
        if self.c == convention.KEYWORDS_LT:
            self.c = self.reader.read(1)
            return Token(convention.TOKEN_LT, convention.KEYWORDS_LT)

        # Equal
        if self.c == convention.KEYWORDS_EQUAL:
            self.c = self.reader.read(1)
            return Token(convention.TOKEN_EQUAL, '=')

        raise error.Error('SyntaxError')
