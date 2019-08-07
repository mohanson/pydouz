import io
import textwrap

import pydouz


def test_func_decl():
    s = textwrap.dedent('''
    def main()
    ''')
    t = pydouz.tokenization.Tokenization(io.StringIO(s))
    assert t.next().kind == pydouz.convention.TOKEN_DEF
    assert t.next().kind == pydouz.convention.TOKEN_IDENTIFIER
    assert t.next().kind == pydouz.convention.TOKEN_L_S_PAREN
    assert t.next().kind == pydouz.convention.TOKEN_R_S_PAREN
