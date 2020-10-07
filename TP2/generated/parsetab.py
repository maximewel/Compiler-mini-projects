
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftADD_OPleftMUL_OPrightUMINUSADD_OP IDENTIFIER MUL_OP NUMBERprogram : statement program : statement ";" programstatement : assignement\n    | expression\n     assignement : IDENTIFIER "=" expression expression : NUMBER\n    | IDENTIFIER expression : \'(\' expression \')\' expression : expression ADD_OP expression \n    | expression MUL_OP expressionexpression : ADD_OP expression %prec UMINUS'
    
_lr_action_items = {'IDENTIFIER':([0,7,8,9,10,11,12,],[5,14,14,5,14,14,14,]),'NUMBER':([0,7,8,9,10,11,12,],[6,6,6,6,6,6,6,]),'(':([0,7,8,9,10,11,12,],[7,7,7,7,7,7,7,]),'ADD_OP':([0,4,5,6,7,8,9,10,11,12,13,14,15,17,18,19,20,],[8,10,-7,-6,8,8,8,8,8,8,10,-7,-11,-9,-10,10,-8,]),'$end':([1,2,3,4,5,6,14,15,16,17,18,19,20,],[0,-1,-3,-4,-7,-6,-7,-11,-2,-9,-10,-5,-8,]),';':([2,3,4,5,6,14,15,17,18,19,20,],[9,-3,-4,-7,-6,-7,-11,-9,-10,-5,-8,]),'MUL_OP':([4,5,6,13,14,15,17,18,19,20,],[11,-7,-6,11,-7,-11,11,-10,11,-8,]),'=':([5,],[12,]),')':([6,13,14,15,17,18,20,],[-6,20,-7,-11,-9,-10,-8,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,9,],[1,16,]),'statement':([0,9,],[2,2,]),'assignement':([0,9,],[3,3,]),'expression':([0,7,8,9,10,11,12,],[4,13,15,4,17,18,19,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> statement','program',1,'p_program','parserAST.py',24),
  ('program -> statement ; program','program',3,'p_programMultiple','parserAST.py',28),
  ('statement -> assignement','statement',1,'p_statement','parserAST.py',32),
  ('statement -> expression','statement',1,'p_statement','parserAST.py',33),
  ('assignement -> IDENTIFIER = expression','assignement',3,'p_assignement','parserAST.py',40),
  ('expression -> NUMBER','expression',1,'p_expression','parserAST.py',44),
  ('expression -> IDENTIFIER','expression',1,'p_expression','parserAST.py',45),
  ('expression -> ( expression )','expression',3,'p_expression_num','parserAST.py',49),
  ('expression -> expression ADD_OP expression','expression',3,'p_expression_op','parserAST.py',53),
  ('expression -> expression MUL_OP expression','expression',3,'p_expression_op','parserAST.py',54),
  ('expression -> ADD_OP expression','expression',2,'p_expression_uminus','parserAST.py',59),
]
