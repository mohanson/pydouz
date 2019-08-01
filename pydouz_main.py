import argparse

import pydouz

parser = argparse.ArgumentParser()
parser.add_argument('src')
parser.add_argument('-o')


def main():
    args = parser.parse_args()

    with open(args.src) as f:
        codegen = pydouz.codegen.CodeGen()
        a = pydouz.tokenization.Tokenization(f)
        a = pydouz.tokenization.TokenizationEmitSpace(a)
        p = pydouz.parser.Parser(a)
        for e in p.parse():
            codegen.code(e)

        codegen.save(args.o)


if __name__ == '__main__':
    main()
