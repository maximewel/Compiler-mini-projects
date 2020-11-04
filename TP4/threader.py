import sys
import os

import ast
from ast import addToClass
from parserast import parse

@addToClass(ast.Node)
def thread(self, lastNode):
    for c in self.children:
        lastNode = c.thread(lastNode)
    lastNode.addNext(self)
    return self


@addToClass(ast.WhileNode)
def thread(self, lastNode):
    beforeCond = lastNode
    exitCond = self.children[0].thread(lastNode)
    exitCond.addNext(self)
    exitBody = self.children[1].thread(self)
    exitBody.addNext(beforeCond.next[-1])
    return self

def thread(tree):
    entry = ast.EntryNode()
    tree.thread(entry)
    return entry

if __name__ == "__main__":
    filename = os.getcwd() + "\\" + sys.argv[1]
    with open(filename) as prog :
        result = parse(prog.read())
        entry = thread(result)

    graph = result.makegraphicaltree()
    entry.threadTree(graph)
    name = os.path.splitext(sys.argv[1])[0] + "threader-ast.pdf"
    graph.write_pdf(name)
    print("file generated : {}".format(name))