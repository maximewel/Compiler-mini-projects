import ply.lex as lex
import sys
import os

tokens = ( 
    'NUMBER', 
    'PLUS', 
    'MINUS'
)

#simple regexes
t_PLUS = r'\+'
t_MINUS = r'-'

#a bit more complex
def t_NUMBER(t) :
    r'\d+'
    t.value = int(t.value)
    return t

#keep trace of the line
def t_newline(t) :
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t) :
    print("illegal char {}".format(t.value))
    t.lexer.skip(1)

lex.lex()

if __name__ == "__main__":
    filename = os.getcwd() + "\\" + sys.argv[1]
    with open(filename) as prog :
        lex.input(prog.read())
        while 1: 
            tok = lex.token()
            if not tok : 
                break 
            print (" line {}: {}({})".format(tok.lineno, tok.type, tok.value))