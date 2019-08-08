import io
import textwrap

import pydouz


def test_expression_func_call():
    s = textwrap.dedent('''
    foo(a, b);
    ''')
    t = pydouz.tokenization.Tokenization(io.StringIO(s))
    p = pydouz.parser.Parser(t)
    a = p.next()
    assert isinstance(a, pydouz.ast.FunctionCall)
    assert isinstance(a.args[0], pydouz.ast.Identifier)
    assert a.args[0].name == 'a'
    assert isinstance(a.args[1], pydouz.ast.Identifier)
    assert a.args[1].name == 'b'


def test_expression_a_add_b():
    s = textwrap.dedent('''
    a b +;
    ''')
    t = pydouz.tokenization.Tokenization(io.StringIO(s))
    p = pydouz.parser.Parser(t)
    a = p.next()
    assert isinstance(a, pydouz.ast.BinaryOperation)
    assert a.operator == pydouz.convention.TOKEN_ADD
    assert isinstance(a.lhs, pydouz.ast.Identifier)
    assert a.lhs.name == 'a'
    assert isinstance(a.rhs, pydouz.ast.Identifier)
    assert a.rhs.name == 'b'


def test_expression_a_sub_1():
    s = textwrap.dedent('''
    a 1 -;
    ''')
    t = pydouz.tokenization.Tokenization(io.StringIO(s))
    p = pydouz.parser.Parser(t)
    a = p.next()
    assert isinstance(a, pydouz.ast.BinaryOperation)
    assert a.operator == pydouz.convention.TOKEN_SUB
    assert isinstance(a.lhs, pydouz.ast.Identifier)
    assert a.lhs.name == 'a'
    assert isinstance(a.rhs, pydouz.ast.Numeric)
    assert a.rhs.n == 1


def test_expression_3_sub_4_add_5():
    s = textwrap.dedent('''
    3 4 - 5 +;
    ''')
    t = pydouz.tokenization.Tokenization(io.StringIO(s))
    p = pydouz.parser.Parser(t)
    a = p.next()
    assert a.operator == pydouz.convention.TOKEN_ADD
    assert isinstance(a.rhs, pydouz.ast.Numeric)
    assert a.rhs.n == 5
    assert isinstance(a.lhs, pydouz.ast.BinaryOperation)
    assert a.lhs.operator == pydouz.convention.TOKEN_SUB
    assert a.lhs.lhs.n == 3
    assert a.lhs.rhs.n == 4


def test_expression_5_1_2_add_4_mul_add_3_sub():
    s = textwrap.dedent('''
    # 5 + ((1 + 2) * 4) - 3
    5 1 2 + 4 * + 3 -;
    ''')
    t = pydouz.tokenization.Tokenization(io.StringIO(s))
    p = pydouz.parser.Parser(t)
    a = p.next()
    assert a.operator == pydouz.convention.TOKEN_SUB
    assert isinstance(a.lhs, pydouz.ast.BinaryOperation)
    assert isinstance(a.lhs.lhs, pydouz.ast.Numeric)
    assert a.lhs.lhs.n == 5
    assert isinstance(a.lhs.rhs, pydouz.ast.BinaryOperation)
    assert a.lhs.rhs.operator == pydouz.convention.TOKEN_MUL
    assert isinstance(a.lhs.rhs.lhs, pydouz.ast.BinaryOperation)
    assert a.lhs.rhs.lhs.operator == pydouz.convention.TOKEN_ADD
    assert isinstance(a.lhs.rhs.lhs.lhs, pydouz.ast.Numeric)
    assert a.lhs.rhs.lhs.lhs.n == 1
    assert a.lhs.rhs.lhs.rhs.n == 2
    assert isinstance(a.lhs.rhs.lhs.rhs, pydouz.ast.Numeric)
    assert isinstance(a.lhs.rhs.rhs, pydouz.ast.Numeric)
    assert a.lhs.rhs.rhs.n == 4
    assert isinstance(a.rhs, pydouz.ast.Numeric)
    assert a.rhs.n == 3


def test_expression_func_call_add_1():
    s = textwrap.dedent('''
    foo(a, b) 1 +;
    ''')
    t = pydouz.tokenization.Tokenization(io.StringIO(s))
    p = pydouz.parser.Parser(t)
    a = p.next()
    assert isinstance(a, pydouz.ast.BinaryOperation)
    assert a.operator == pydouz.convention.TOKEN_ADD
    assert isinstance(a.lhs, pydouz.ast.FunctionCall)
    assert isinstance(a.rhs, pydouz.ast.Numeric)


def test_expression_func_call_add_func_call():
    s = textwrap.dedent('''
    foo(a, b) foo(c, d) +;
    ''')
    t = pydouz.tokenization.Tokenization(io.StringIO(s))
    p = pydouz.parser.Parser(t)
    a = p.next()
    assert isinstance(a, pydouz.ast.BinaryOperation)
    assert isinstance(a.lhs, pydouz.ast.FunctionCall)
    assert isinstance(a.rhs, pydouz.ast.FunctionCall)


def test_expression_func_call_with_expression():
    s = textwrap.dedent('''
    foo(a b +, 1);
    ''')
    t = pydouz.tokenization.Tokenization(io.StringIO(s))
    p = pydouz.parser.Parser(t)
    a = p.next()
    assert isinstance(a, pydouz.ast.FunctionCall)
    assert isinstance(a.args[0], pydouz.ast.BinaryOperation)
    assert isinstance(a.args[1], pydouz.ast.Numeric)


def test_expression_gt():
    s = textwrap.dedent('''
    a 1 >;
    ''')
    t = pydouz.tokenization.Tokenization(io.StringIO(s))
    p = pydouz.parser.Parser(t)
    a = p.next()
    assert isinstance(a, pydouz.ast.BinaryOperation)
    assert a.operator == pydouz.convention.TOKEN_GT
    assert isinstance(a.lhs, pydouz.ast.Identifier)
    assert isinstance(a.rhs, pydouz.ast.Numeric)


def test_expression_lt():
    s = textwrap.dedent('''
    a 1 <;
    ''')
    t = pydouz.tokenization.Tokenization(io.StringIO(s))
    p = pydouz.parser.Parser(t)
    a = p.next()
    assert isinstance(a, pydouz.ast.BinaryOperation)
    assert a.operator == pydouz.convention.TOKEN_LT
    assert isinstance(a.lhs, pydouz.ast.Identifier)
    assert isinstance(a.rhs, pydouz.ast.Numeric)


def test_expression_if():
    s = textwrap.dedent('''
    if a b > { 1; } else { 0; };
    ''')
    t = pydouz.tokenization.Tokenization(io.StringIO(s))
    p = pydouz.parser.Parser(t)
    a = p.next()
    assert isinstance(a, pydouz.ast.If)
    assert isinstance(a.cond, pydouz.ast.BinaryOperation)
    assert isinstance(a.if_then, pydouz.ast.Block)
    assert isinstance(a.if_else, pydouz.ast.Block)


def test_block_0():
    s = textwrap.dedent('''
    {
        a b +;
        a b -;
    }
    ''')
    t = pydouz.tokenization.Tokenization(io.StringIO(s))
    p = pydouz.parser.Parser(t)
    a = p.next()
    assert isinstance(a.data[0], pydouz.ast.BinaryOperation)
    assert isinstance(a.data[1], pydouz.ast.BinaryOperation)


def test_block_1():
    s = textwrap.dedent('''
    {
        let a = 1 1 +;
        a;
    }
    ''')
    t = pydouz.tokenization.Tokenization(io.StringIO(s))
    p = pydouz.parser.Parser(t)
    a = p.next()
    assert isinstance(a.data[0], pydouz.ast.Let)
    assert isinstance(a.data[1], pydouz.ast.Identifier)


def test_func_defn():
    s = textwrap.dedent('''
    def foo(a, b) {
        a b +;
    }
    ''')
    t = pydouz.tokenization.Tokenization(io.StringIO(s))
    p = pydouz.parser.Parser(t)
    a = p.next()
    assert isinstance(a, pydouz.ast.FunctionDefn)
    assert a.func_decl.func_name == 'foo'
    assert a.func_decl.args[0].name == 'a'
    assert a.func_decl.args[1].name == 'b'
    assert isinstance(a.body, pydouz.ast.Block)


def test_let():
    s = textwrap.dedent('''
    let a = 1 1 +;
    ''')
    t = pydouz.tokenization.Tokenization(io.StringIO(s))
    p = pydouz.parser.Parser(t)
    a = p.next()
    assert isinstance(a, pydouz.ast.Let)
    assert a.identifier.name == 'a'
    assert a.expression.operator == pydouz.convention.TOKEN_ADD
