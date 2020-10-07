# coding: latin-1
''' AST.py, version 0.2

Petit module utilitaire pour la construction, la manipulation et la 
représentation d'arbres syntaxiques abstraits.

Sûrement plein de bugs et autres surprises. À prendre comme un 
"work in progress"...
Notamment, l'utilisation de pydot pour représenter un arbre syntaxique cousu
est une utilisation un peu "limite" de graphviz. Ça marche, mais le layout n'est
pas toujours optimal...

2008-2009, Matthieu Amiguet, HE-Arc
'''

import pydot

class Node:
    count = 0
    type = 'Node (unspecified)'
    shape = 'ellipse'
    def __init__(self,children=None):
        self.ID = str(Node.count)
        Node.count+=1
        if not children: self.children = []
        elif hasattr(children,'__len__'):
            self.children = children
        else:
            self.children = [children]

    def asciitree(self, prefix=''):
        result = "%s%s\n" % (prefix, repr(self))
        prefix += '|  '
        for c in self.children:
            if not isinstance(c,Node):
                result += "%s*** Error: Child of type %r: %r\n" % (prefix,type(c),c)
                continue
            result += c.asciitree(prefix)
        return result
    
    def __str__(self):
        return self.asciitree()
    
    def __repr__(self):
        return self.type
    
    def makegraphicaltree(self, dot=None, edgeLabels=True):
            if not dot: dot = pydot.Dot()
            dot.add_node(pydot.Node(self.ID,label=repr(self), shape=self.shape))
            label = edgeLabels and len(self.children)-1
            for i, c in enumerate(self.children):
                c.makegraphicaltree(dot, edgeLabels)
                edge = pydot.Edge(self.ID,c.ID)
                if label:
                    edge.set_label(str(i))
                dot.add_edge(edge)
                #Workaround for a bug in pydot 1.0.2 on Windows:
                dot.set_graphviz_executables({'dot': r'C:\Program Files (x86)\Graphviz2.38\bin\dot.exe'})
            return dot
        
class ProgramNode(Node):
    type = 'Program'
        
class TokenNode(Node):
    type = 'token'
    def __init__(self, tok):
        Node.__init__(self)
        self.tok = tok
        
    def __repr__(self):
        return repr(self.tok)
    
class OpNode(Node):
    def __init__(self, op, children):
        Node.__init__(self,children)
        self.op = op
        try:
            self.nbargs = len(children)
        except AttributeError:
            self.nbargs = 1
        
    def __repr__(self):
        return "%s (%s)" % (self.op, self.nbargs)
    
class AssignNode(Node):
    type = '='