from . import convention


class Token:
    def __init__(self, kind: int, s: str):
        self.kind = kind
        self.s = s

    def __repr__(self):
        if self.kind == convention.TOKEN_EOF:
            return f'Token: EOF'
        if self.kind == convention.TOKEN_EOL:
            return f'Token: EOL'
        if self.kind == convention.TOKEN_SPACE:
            return f'Token: Space {len(self.s)}'
        if self.kind == convention.TOKEN_NUMBER:
            return f'Token: Number {self.s}'
        if self.kind == convention.TOKEN_IDENTIFIER:
            return f'Token: Identifier {self.s}'
        if self.kind == convention.TOKEN_L_PARAN:
            return f'Token: Paran {convention.KEYWORDS_L_PAREN}'
        if self.kind == convention.TOKEN_R_PARAN:
            return f'Token: Paran {convention.KEYWORDS_R_PAREN}'
        if self.kind == convention.TOKEN_COMMA:
            return f'Token: Comma {convention.KEYWORDS_COMMA}'
        if self.kind == convention.TOKEN_COLON:
            return f'Token: Colon {convention.KEYWORDS_COLON}'
        if self.kind == convention.TOKEN_ADD:
            return f'Token: Add {convention.KEYWORDS_ADD}'
        if self.kind == convention.TOKEN_SUB:
            return f'Token: Sub {convention.KEYWORDS_SUB}'
        if self.kind == convention.TOKEN_MUL:
            return f'Token: MUL {convention.KEYWORDS_MUL}'
        if self.kind == convention.TOKEN_DIV:
            return f'Token: DIV {convention.KEYWORDS_DIV}'
        if self.kind == convention.TOKEN_GT:
            return f'Token: GT {convention.KEYWORDS_GT}'
        if self.kind == convention.TOKEN_LT:
            return f'Token: LT {convention.KEYWORDS_LT}'
        if self.kind == convention.TOKEN_DEF:
            return f'Token: Def'
        if self.kind == convention.TOKEN_RETURN:
            return f'Token: Return'
        if self.kind == convention.TOKEN_IF:
            return f'Token: If'
        if self.kind == convention.TOKEN_ELSE:
            return f'Token: Else'
        if self.kind == convention.TOKEN_OTHER:
            return f'Token: Other {self.s}'
        return f'Token: ???? {self.s}'
