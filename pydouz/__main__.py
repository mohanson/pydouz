import argparse

from . import driver

parser = argparse.ArgumentParser()
parser.add_argument('src')
parser.add_argument('-o')

args = parser.parse_args()

driver = driver.User()
driver.compile(args.src, args.o)
