import ast
from ast import addToClass
from functools import reduce
from parserast import parse
import sys
import os


#init ops and vars
ops = {
    '+' : 'ADD',
    '-' : 'SUB',
    '*' : 'MUL',
    '/' : 'DIV',
}

def whilecounter():
    whilecounter.current += 1
    return whilecounter.current
whilecounter.current = 0

#programme
@addToClass(ast.ProgramNode)
def compile(self):
    bytecode = ""
    for c in self.children:
        bytecode += c.compile()
    return bytecode

#node variable
@addToClass(ast.TokenNode)
def compile(self):
    bytecode = ""
    if isinstance(self.tok, str):
        bytecode += "PUSHV %s\n" % self.tok
    else:
        bytecode += "PUSHC %s\n" % self.tok
    return bytecode

@addToClass(ast.AssignNode)
def compile(self):
    bytecode = ""
    bytecode += self.children[1].compile()
    bytecode += "SET %s\n" % self.children[0].tok
    return bytecode
    
#print
@addToClass(ast.PrintNode)
def compile(self):
    bytecode = ""
    bytecode += self.children[0].compile()
    bytecode += "PRINT\n"
    return bytecode
    
#operation
@addToClass(ast.OpNode)
def compile(self):
    bytecode = ""
    if len(self.children) == 1:
        bytecode += self.children[0].compile()
        bytecode += "USUB\n"
    else:
        for c in self.children:
            bytecode += c.compile()
        bytecode += ops[self.op] + "\n"
    return bytecode
    
#while
@addToClass(ast.WhileNode)
def compile(self):
    counter = whilecounter()
    bytecode = ""
    bytecode += "JMP cond%s\n" % counter
    bytecode += "body%s: " % counter
    bytecode += self.children[1].compile()
    bytecode += "cond%s: " % counter
    bytecode += self.children[0].compile()
    bytecode += "JINZ body%s\n" % counter
    return bytecode

if __name__ == "__main__":
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    compiled = ast.compile()
    name = os.path.splitext(sys.argv[1])[0]+'.vm'
    outfile = open(name,'w')
    outfile.write(compiled)
    outfile.close()
    print("Wrote output to",name)
