import argparse

import pydouz

parser = argparse.ArgumentParser()
parser.add_argument('src')
parser.add_argument('-o')


def main():
    args = parser.parse_args()
    pydouz.driver.make(args.src, args.o)

if __name__ == '__main__':
    main()
