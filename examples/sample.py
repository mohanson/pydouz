import pydouz

with open('./examples/sample.dz') as f:
    codegen = pydouz.codegen.CodeGen()

    a = pydouz.tokenization.Tokenization(f)
    a = pydouz.tokenization.TokenizationEmitSpace(a)

    # for t in a.iter():
    #     print(t)

    p = pydouz.parser.Parser(a)
    for e in p.parse():
        r = codegen.code(e)

    codegen.save('/tmp/output.ll')

# r = codegen.code(pydouz.ast.Binop(pydouz.convention.TOKEN_ADD, pydouz.ast.Number(10), pydouz.ast.Var('a')  ))
# print(r)
