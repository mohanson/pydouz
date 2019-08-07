import collections
import typing

from . import common
from . import convention
from . import token


class Tokenization:
    def __init__(self, reader: typing.TextIO):
        self.reader = reader
        self.buffer = collections.deque([], convention.TOKEN_BUFFER_SIZE)
        self.c = ''

    def iter(self):
        for _ in common.Loop():
            r = self.next()
            if r.kind == convention.TOKEN_EOF:
                return
            yield r

    def next(self):
        t = self.take()
        # Remove all spaces that are not at the beginning of the line
        if t.kind == convention.TOKEN_SPACE:
            if self.buffer[-1].kind != convention.TOKEN_EOL:
                return self.next()
        # Remove extra line breaks
        if t.kind == convention.TOKEN_EOL:
            if self.buffer[-1].kind == convention.TOKEN_EOL:
                return self.next()
        self.buffer.append(t)
        return t

    def back(self, i: int):
        return self.buffer[convention.TOKEN_BUFFER_SIZE - i]

    def take(self):
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
            if s == convention.KEYWORDS_IF:
                return token.Token(convention.TOKEN_IF, s)
            if s == convention.KEYWORDS_ELSE:
                return token.Token(convention.TOKEN_ELSE, s)
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
            return self.take()

        # L_Paren:
        if self.c == convention.KEYWORDS_L_PAREN:
            self.c = self.reader.read(1)
            return token.Token(convention.TOKEN_L_PARAN, convention.KEYWORDS_L_PAREN)

        # R_Paren:
        if self.c == convention.KEYWORDS_R_PAREN:
            self.c = self.reader.read(1)
            return token.Token(convention.TOKEN_R_PARAN, convention.KEYWORDS_R_PAREN)

        # Comma
        if self.c == convention.KEYWORDS_COMMA:
            self.c = self.reader.read(1)
            return token.Token(convention.TOKEN_COMMA, convention.KEYWORDS_COMMA)

        # Colon
        if self.c == convention.KEYWORDS_COLON:
            self.c = self.reader.read(1)
            return token.Token(convention.TOKEN_COLON, convention.KEYWORDS_COLON)

        # Add
        if self.c == convention.KEYWORDS_ADD:
            self.c = self.reader.read(1)
            return token.Token(convention.TOKEN_ADD, convention.KEYWORDS_ADD)

        # Sub
        if self.c == convention.KEYWORDS_SUB:
            self.c = self.reader.read(1)
            return token.Token(convention.TOKEN_SUB, convention.KEYWORDS_SUB)

        # Mul
        if self.c == convention.KEYWORDS_MUL:
            self.c = self.reader.read(1)
            return token.Token(convention.TOKEN_MUL, convention.KEYWORDS_MUL)

        # Div
        if self.c == convention.KEYWORDS_DIV:
            self.c = self.reader.read(1)
            return token.Token(convention.TOKEN_DIV, convention.KEYWORDS_DIV)

        # GT
        if self.c == convention.KEYWORDS_GT:
            self.c = self.reader.read(1)
            return token.Token(convention.TOKEN_GT, convention.KEYWORDS_GT)

        # LT
        if self.c == convention.KEYWORDS_LT:
            self.c = self.reader.read(1)
            return token.Token(convention.TOKEN_LT, convention.KEYWORDS_LT)

        raise ''
