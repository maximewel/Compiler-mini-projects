import ast
from parserast import parse
from threader import thread
import sys

#init ops and vars
ops = {
    '+' : lambda x,y : x+y,
    '-' : lambda x,y : x-y,
    '*' : lambda x,y : x*y,
    '/' : lambda x,y : x/y,
}

stack = []
vars = {}

def valueOfToken(t):
    if isinstance(t, str):
        try:
            return vars[t]
        except KeyError:
            print(f"Error : variable {t} undefined !")
    return t

def execute(node):
    while node:
        if node.__class__ in [ast.EntryNode, ast.ProgramNode]:
            pass
        elif node.__class__ == ast.TokenNode:
            stack.append(node.tok)
        elif node.__class__ == ast.PrintNode:
            val = stack.pop()
            print(valueOfToken(val))
        elif node.__class__== ast.OpNode:
            arg2 = valueOfToken(stack.pop())
            if node.nbargs == 2:
                arg1 = valueOfToken(stack.pop())
            else:
                arg1 = 0
            stack.append(ops[node.op](arg1, arg2))
        elif node.__class__ == ast.AssignNode:
            val = valueOfToken(stack.pop())
            name = stack.pop()
            vars[name] = val
        elif node.__class__ == ast.WhileNode:
            cond = valueOfToken(stack.pop())
            if cond:
                node = node.next[0]
            else:
                node = node.next[1]
            continue
        if node.next:
            node = node.next[0]
        else:
            node = None

if __name__ == "__main__":
    prog = open(sys.argv[1]).read()
    astree = parse(prog)
    entry = thread(astree)
    execute(entry)