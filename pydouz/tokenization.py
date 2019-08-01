import typing

from . import common
from . import convention
from . import token


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

    def next(self):
        if not self.c:
            self.c = self.reader.read(1)

        # EOF
        if not self.c:
            return token.Token(convention.TOKEN_EOF, '')

        s = ''

        # SPACE
        if self.c == convention.KEYWORDS_SPACE:
            s += self.c
            for _ in common.Long():
                self.c = self.reader.read(1)
                if self.c == convention.KEYWORDS_SPACE:
                    s += self.c
                    continue
                break
            return token.Token(convention.TOKEN_SPACE, s)

        # EOL
        if self.c == convention.KEYWORDS_EOL:
            s += self.c
            self.c = self.reader.read(1)
            return token.Token(convention.TOKEN_EOL, s)

        # Identifier && keywords
        if self.c.isalpha():
            s = self.c
            for _ in common.Long():
                self.c = self.reader.read(1)
                if self.c.isalnum():
                    s += self.c
                    continue
                break

            if s == convention.KEYWORDS_DEF:
                return token.Token(convention.TOKEN_DEF, s)
            if s == convention.KEYWORDS_RETURN:
                return token.Token(convention.TOKEN_RETURN, s)
            return token.Token(convention.TOKEN_IDENTIFIER, s)

        # Number
        if self.c.isdigit():
            s += self.c
            self.c = self.reader.read(1)
            for _ in common.Long():
                if self.c.isdigit():
                    s += self.c
                    self.c = self.reader.read(1)
                    continue
                break
            return token.Token(convention.TOKEN_NUMBER, s)

        # Comment
        if self.c == convention.KEYWORDS_COMMENT:
            for _ in common.Long():
                self.c = self.reader.read(1)
                if self.c == convention.KEYWORDS_EOL:
                    break
                continue
            return self.next()

        # L_Paren:
        if self.c == convention.KEYWORDS_L_PAREN:
            self.c = self.reader.read(1)
            return token.Token(convention.TOKEN_L_PARAN, self.c)

        # R_Paren:
        if self.c == convention.KEYWORDS_R_PAREN:
            self.c = self.reader.read(1)
            return token.Token(convention.TOKEN_R_PARAN, self.c)

        # Comma
        if self.c == convention.KEYWORDS_COMMA:
            self.c = self.reader.read(1)
            return token.Token(convention.TOKEN_COMMA, self.c)

        # Colon
        if self.c == convention.KEYWORDS_COLON:
            self.c = self.reader.read(1)
            return token.Token(convention.TOKEN_COLON, self.c)

        # Add
        if self.c == convention.KEYWORDS_ADD:
            self.c = self.reader.read(1)
            return token.Token(convention.TOKEN_ADD, self.c)

        # Sub
        if self.c == convention.KEYWORDS_SUB:
            self.c = self.reader.read(1)
            return token.Token(convention.TOKEN_SUB, self.c)

        # Mul
        if self.c == convention.KEYWORDS_MUL:
            self.c = self.reader.read(1)
            return token.Token(convention.TOKEN_MUL, self.c)

        # Div
        if self.c == convention.KEYWORDS_DIV:
            self.c = self.reader.read(1)
            return token.Token(convention.TOKEN_DIV, self.c)

        raise ''


class TokenizationEmitSpace:
    def __init__(self, tokenization: Tokenization):
        self.tokenization = tokenization
        self.t = self.tokenization.next()

    def iter(self):
        r = self.next()
        yield r
        if r.kind == convention.TOKEN_EOF:
            return
        yield from self.iter()

    def next(self):
        for _ in common.Long():
            if self.t.kind == convention.TOKEN_SPACE:
                self.t = self.tokenization.next()
                continue
            if self.t.kind == convention.TOKEN_COMMA:
                self.t = self.tokenization.next()
                continue
            if self.t.kind == convention.TOKEN_EOF:
                return self.t

            r = self.t
            self.t = self.tokenization.next()
            return r
