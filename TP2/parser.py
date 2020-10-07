import ply.lex as lex
import ply.yacc as yacc
import sys
import os

from lex import tokens

operations = {
    "+"   : lambda x,y: x+y,
    "-"   : lambda x,y: x-y,
    "*"   : lambda x,y: x*y,
    "/"   : lambda x,y: x/y,
}

precedence = (
    ("left", "ADD_OP"),
    ("left", "MUL_OP"),
    ('right', 'UMINUS'),
)


def p_program(p) :
    '''program : statement
    | statement ";" program'''
    p[0] = p[len(p)-1] #only return last program at the end

def p_statement(p) :
    '''statement : assignement
    | expression
    '''
    p[0] = p[1]

def p_assignement(p) :
    ''' assignement : VAR "=" expression '''
    variables[p[1]] = p[3]
    p[0] = p[3]

def p_expression(p) :
    '''expression : NUMBER
    | VAR'''
    try :
        p[0] = variables[p[1]]
    except :
        p[0] = p[1]

def p_expression_num(p) :
    ''' expression : '(' expression ')' '''
    p[0] = p[2]

def p_expression_op(p) :
    '''expression : expression ADD_OP expression 
    | expression MUL_OP expression'''
    p[0] = operations[p[2]](p[1], p[3])

def p_expression_uminus(p):
    '''expression : ADD_OP expression %prec UMINUS'''
    p[0] = operations[p[1]](0, p[2])

def p_error(p) :
    print("syntax error in line {}".format(p.lineno))
    parser.errok()

parser = yacc.yacc(outputdir = "generated")
variables = {}

if __name__ == "__main__":
    filename = os.getcwd() + "\\" + sys.argv[1]
    with open(filename) as prog :
        result = yacc.parse(prog.read())
        print(result)