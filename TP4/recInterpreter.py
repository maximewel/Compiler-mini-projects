import ast
from ast import addToClass
from functools import reduce
from parserast import parse
import sys


#init ops and vars
ops = {
    '+' : lambda x,y : x+y,
    '-' : lambda x,y : x-y,
    '*' : lambda x,y : x*y,
    '/' : lambda x,y : x/y,
}
vars = {}

#interpret functions
@addToClass(ast.ProgramNode)
def execute(self):
    for c in self.children:
        c.execute()

@addToClass(ast.TokenNode)
def execute(self):
    if isinstance(self.tok, str):
        try:
            return vars[self.tok]
        except KeyError:
            print(f"Error : Variable {self.tok} undefined !")
    return self.tok

@addToClass(ast.OpNode)
def execute(self):
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0,0)
    return reduce(ops[self.op], args)

@addToClass(ast.AssignNode)
def execute(self):
    vars[self.children[0].tok] = self.children[1].execute()

@addToClass(ast.PrintNode)
def execute(self):
    print(self.children[0].execute())

@addToClass(ast.WhileNode)
def execute(self):
    while(self.children[0].execute()):
        self.children[1].execute()

if __name__ == "__main__":
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    ast.execute()