import ply.lex as lex
import ply.yacc as yacc
import sys
import os

from lex import tokens
import ast

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
    '''program : statement '''
    p[0] = ast.ProgramNode(p[1])

def p_programMultiple(p) :
    '''program : statement ";" program'''
    p[0] = ast.ProgramNode([p[1]] + p[3].children)

def p_statement(p) :
    '''statement : assignement
    | expression
    '''
    #p[0] = ast.Node(p[1])
    p[0] = p[1]


def p_assignement(p) :
    ''' assignement : IDENTIFIER "=" expression '''
    p[0] = ast.AssignNode([ast.TokenNode(p[1]), p[3]])

def p_expression(p) :
    '''expression : NUMBER
    | IDENTIFIER'''
    p[0] = ast.TokenNode(p[1])

def p_expression_num(p) :
    ''' expression : '(' expression ')' '''
    p[0] = ast.TokenNode(p[2])

def p_expression_op(p) :
    '''expression : expression ADD_OP expression 
    | expression MUL_OP expression'''
    # Stock into AST graph
    p[0] = ast.OpNode(p[2], [p[1], p[3]])

def p_expression_uminus(p):
    '''expression : ADD_OP expression %prec UMINUS'''
    p[0] = ast.OpNode(p[1], [0, p[2]])

def p_error(p) :
    print("syntax error in line {}".format(p.lineno))
    parser.errok()

parser = yacc.yacc(outputdir = "generated")

if __name__ == "__main__":
    filename = os.getcwd() + "\\" + sys.argv[1]
    with open(filename) as prog :
        result = yacc.parse(prog.read())
        print(result)
    graph=result.makegraphicaltree()
    name = os.path.splitext(sys.argv[1])[0] + "-ast.pdf"
    graph.write_pdf(name)
    print("file generated : {}".format(name))