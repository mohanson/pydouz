IDENTIFIER_LEN_LIMIT = 1 << 32
TOKEN_BUFFER_SIZE = 4

enum = iter(range(256))

TOKEN_EOF = next(enum)
TOKEN_EOL = next(enum)
TOKEN_SPACE = next(enum)
TOKEN_NUMBER = next(enum)
TOKEN_IDENTIFIER = next(enum)
TOKEN_L_PARAN = next(enum)
TOKEN_R_PARAN = next(enum)
TOKEN_COMMA = next(enum)
TOKEN_COLON = next(enum)
TOKEN_ADD = next(enum)
TOKEN_SUB = next(enum)
TOKEN_MUL = next(enum)
TOKEN_DIV = next(enum)
TOKEN_GT = next(enum)
TOKEN_LT = next(enum)
TOKEN_DEF = next(enum)
TOKEN_RETURN = next(enum)
TOKEN_IF = next(enum)
TOKEN_ELSE = next(enum)
TOKEN_OTHER = next(enum)

KEYWORDS_EOL = '\n'
KEYWORDS_SPACE = ' '
KEYWORDS_L_PAREN = '('
KEYWORDS_R_PAREN = ')'
KEYWORDS_COMMA = ','
KEYWORDS_COLON = ':'
KEYWORDS_ADD = '+'
KEYWORDS_SUB = '-'
KEYWORDS_MUL = '*'
KEYWORDS_DIV = '/'
KEYWORDS_GT = '>'
KEYWORDS_LT = '<'
KEYWORDS_DEF = 'def'
KEYWORDS_RETURN = 'return'
KEYWORDS_IF = 'if'
KEYWORDS_ELSE = 'or'
KEYWORDS_COMMENT = '#'

GLOBAL_GCC = 'gcc'
GLOBAL_LLC = 'llc'
GLOBAL_LLI = 'lli'
GLOBAL_LLVM_AS = 'llvm-as'
