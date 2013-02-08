
# def func_op(op, *operands):
#     """Apply the string representation of the operator symbol op to the
#     operands.

#     >>> func_op('-', -2)
#     2
#     >>> func_op('+', 1, 1)
#     2

#     Documentation on all the python operators can be found at
#     http://docs.python.org/2/library/operator.html
#     """
#     symbol_map = {
#         # unary operators
#         ('not', 1): lambda o: not o,
#         ('~', 1): lambda o: ~ o,
#         ('del', 1): lambda o: del o,
#         ('-', 1): lambda o: - o,
#         # binary operators
#         ('<', 2): lambda l, r: l < r,
#         ('<=', 2): lambda l, r: l <= r,
#         ('==', 2): lambda l, r: l == r,
#         ('!=', 2): lambda l, r: l != r,
#         ('>=', 2): lambda l, r: l >= r,
#         ('>', 2): lambda l, r: l > r,
#         ('+', 2): lambda l, r: l + r,
#         ('&', 2): lambda l, r: l & r,
#         ('/', 2): lambda l, r: l / r,
#         ('//', 2): lambda l, r: l // r,
#         ('is', 2): lambda l, r: l is r,
#         ('is not', 2): lambda l, r: l is not r,
#         ('%', 2): lambda l, r: l % r,
#         ('*', 2): lambda l, r: l * r,
#         ('|', 2): lambda l, r: l | r,
#         ('**', 2): lambda l, r: l ** r,
#         ('-', 2): lambda l, r: l - r,
#         ('^', 2): lambda l, r: l ^ r,
#         ('in', 2): lambda l, r: l in r,
#     }

#     return symbol_map[(op, len(operands))](*operands)

# print func_op('!=', 2, 2) # false
# print func_op('~', 7) # -8
# print func_op('+', [1, 2], [3, 4]) # [1, 2, 3, 4]

# from ast import literal_eval

# def eval_op(op, *operands):
#     if len(operands) == 1:
#         exp = '{op}{operands[0]}'
#     elif len(operands) == 2:
#         exp = '{operands[0]} {op} {operands[1]}'
#     else:
#         raise Exception('only unary and binary operators are handled')
#     expression = exp.format(op=op, operands=operands)
#     print expression
#     return literal_eval(expression)

# print eval_op('1,', '2,', '2,') # false
# print eval_op(1, 7) # -8

# for label in ('<', '<=', '==', '>=', '!='):
#     for check in ((0,0), (0,1), (1,0)):
#         print('{check[0]} {label} {check[1]}: {result}'.format(
#             check=check, label=label, result=bin_operator(label, *check)))

import ast
"""
check to see if it's an expression. if not, bail.
if it's an expression. if not, bail.
build and eval the expression
"""

# class _FindTheOp(ast.NodeVisitor):
#     """Find the operator, and complain if more than one is found"""
#     def __init__(self, *args, **kwargs):
#         super(_FindTheOp, self).__init__(*args, **kwargs)
#         self.expressions = []
#         self.operators = []

#     def visit_Expr(self, node):
#         print 'adding expression', ast.dump(node)
#         self.expressions.append(node)

#     def visit_UnaryOp(self, node):
#         print 'adding unary op', ast.dump(node)
#         self.operators.append(node)

#     def visit_BinOp(self, node):
#         print 'adding binary op', ast.dump(node)
#         self.operators.append(node)

#     def verify(self, node):
#         self.visit(node)
#         if len(self.expressions) != 1:
#             for expression in self.expressions:
#                 print ast.dump(expression)
#             raise ValueError('only one operation allowed')

#         return self.expressions[0]
#     # def visit_UnaryOp(self, node):
#     #     ops.append(node)
#     # def visit_BinOp(self, node):
    #     ops.append(node)



# def func_op(op, *operands):

#     expression = {
#         1: '{op} ({operands[0]})',
#         2: '{operands[0]} {op} ({operands[1]})'
#     }[len(operands)].format(op=op, operands=operands)
    
#     expr = ast.parse(expression).body[0]

#     print ast.dump(expr)


"""
1. get the operator by re-extracting it from an ast bin/unary op with safe vals
2. get the value safely by running it through literal_eval
3. build an expression with ast.Expression
4. eval and return
"""
sentinel = object()

def func_op(op, left, right=sentinel):
    """all values are suspicious"""
    # get the operator by extracting it from a parsed string with safe values
    safety_op_test = '0 {} (0)'.format(op) if right is not sentinel else '{} (0)'.format(op)
    safety_ast = ast.parse(safety_op_test)
    safe_op = safety_ast.body[0].value.__class__
    if isinstance(safe_op(), ast.BinOp):
        TYPE = 'binop'
        safe_op = safety_ast.body[0].value.op.__class__
    elif isinstance(safe_op(), ast.UnaryOp):
        TYPE = 'unaryop'
        safe_op = safety_ast.body[0].value.op.__class__
    elif isinstance(safe_op(), ast.BoolOp):
        TYPE = 'boolop'
        safe_op = safety_ast.body[0].value.op.__class__
    elif isinstance(safe_op(), ast.Compare):
        TYPE = 'compare'
        safe_op = safety_ast.body[0].value.ops[0].__class__
    else:
        print safe_op
        raise TypeError('the node is not a UnaryOp, BinaryOp, or Compare')

    # use literal_eval to ensure the operands are safe
    safe_left = ast.literal_eval(str(left))
    left_thing = ast.parse(str(safe_left)).body[0].value
    if TYPE is not 'unaryop':
        safe_right = ast.literal_eval(str(right))
        right_thing = ast.parse(str(safe_right)).body[0].value

    # build an expression with the safetied inputs
    safe_node = ast.Expression(ast.UnaryOp(
            safe_op(),
            left_thing,
        ) if TYPE is 'unaryop' else ast.BinOp(
            left_thing,
            safe_op(),
            right_thing,
        ) if TYPE is 'binop' else ast.BoolOp(
            op = safe_op(),
            values = [left_thing, right_thing]
        ) if TYPE is 'boolop' else ast.Compare(
            left=left_thing,
            ops=[safe_op()],
            comparators=[right_thing],
        ) if TYPE is 'compare' else None
    )

    fixed_node = ast.fix_missing_locations(safe_node)
    code_obj = compile(fixed_node, '<string>', 'eval')
    result = eval(code_obj)

    return result




def func_op2(op, *operands):
    build_args = lambda op_class, op, *operands: {
        ast.UnaryOp : {'op': op(), 'operand': operands[0]},
        ast.BinOp: {'left': operands[0], 'op': op(), 'right': oprerands[1]},
        ast.BoolOp: {'op': op(), 'values': operands},
        ast.Compare: {'left': operands[0], 'ops': [op()], 'comparators': [operands[2]]},
    }[op_class]    





### TEST BINARIES
bin_ops = ('+', '-', '/', '//', '&', '|', '*', '**', '<<', 'is', 'is not')
vals = ((0, 1), (1, 1), (-1, 1))

for op in bin_ops:
    for val in vals:
        func_op(op, *val)

cmp_ops = ('<', '<=', '==', '!=', '>=', '>')
for op in cmp_ops:
    for val in vals:
        func_op(op, *val)

bool_ops = ('or', 'and')
vals = (True, False, 0, 1, 2, -1)
for op in bool_ops:
    for o1 in vals:
        for o2 in vals:
            func_op(op, o1, o2)

un_ops = ('-', '+', '~', 'not')
vals = (0, -1, 1)
for op in un_ops:
    for val in vals:
         func_op(op, val)


# print func_op('&', 3, 5) # 1
# print func_op('-', -4) # 4
# print func_op('<=', 2, 2) # True
# print func_op('and', False, False)
# print func_op('and', 3, 2)
#print func_op('+', 3, '4 + 5')




