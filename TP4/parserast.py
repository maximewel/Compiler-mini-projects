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

def p_statement(p):
    '''statement : assignement
    | structure
    | print
    '''
    p[0] = p[1]

def p_print(p):
    ''' print : PRINT expression '''
    p[0] = ast.PrintNode(p[2])

def p_structure(p):
    ''' structure : WHILE expression "{" program "}" '''
    p[0] = ast.WhileNode([p[2], p[4]])

def p_assignement(p):
    ''' assignement : IDENTIFIER "=" expression '''
    p[0] = ast.AssignNode([ast.TokenNode(p[1]), p[3]])

def p_expression(p) :
    '''expression : NUMBER
    | IDENTIFIER'''
    p[0] = ast.TokenNode(p[1])

def p_expression_num(p) :
    ''' expression : '(' expression ')' '''
    p[0] = p[2]

def p_expression_op(p) :
    '''expression : expression ADD_OP expression 
    | expression MUL_OP expression'''
    p[0] = ast.OpNode(p[2], [p[1], p[3]])

def p_expression_uminus(p):
    '''expression : ADD_OP expression %prec UMINUS'''
    #p[0] = ast.OpNode(p[1], [0, p[2]])                     #faux : insert 0
    #p[0] = ast.OpNode(p[1], [ast.TokenNode(0), p[2]])      #correct binaire : insert tokenNode(0)
    p[0] = ast.OpNode(p[1], [p[2]])                         #correct unaire : insert tokenNode(0)


def p_error(p) :
    print("syntax error in line {}".format(p.lineno))
    parser.errok()

parser = yacc.yacc(outputdir = "generated")

if __name__ == "__main__":
    filename = os.getcwd() + "\\" + sys.argv[1]
    with open(filename) as prog :
        result = yacc.parse(prog.read())
        print(result)
    graph = result.makegraphicaltree()
    name = os.path.splitext(sys.argv[1])[0] + "-ast.pdf"
    graph.write_pdf(name)
    print("file generated : {}".format(name))

def parse(program):
    result = yacc.parse(program)
    return result