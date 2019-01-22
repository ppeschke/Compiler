class AST(object):
	pass

class BinOp(AST):
	def __init__(self, left, op, right):
		self.left = left
		self.token = self.op = op
		self.right = right
	
class Num(AST):
	def __init__(self, token):
		self.token = token
		self.value = token.value

class UnaryOp(AST):
	def __init__(self, op, identifier):
		self.token = self.op = op
		self.identifier = identifier

class Compound(AST):
	def __init__(self):
		self.children = []

class Assign(AST):
	def __init__(self, left, op, right):
		self.left = left
		self.token = self.op = op
		self.right = right

class Var(AST):
	def __init__(self, token, index):
		self.token = token
		self.var_name = token.value
		self.index = index

class Indexer(AST):
	def __init__(self, token):
		self.token = token
		self.value = token.value

class Loop(AST):
	def __init__(self, token, condition, body):
		self.token = token
		self.condition = condition
		self.body = body

class If(AST):
	def __init__(self, token, condition, body, else_node):
		self.token = token
		self.condition = condition
		self.body = body
		self.else_node = else_node

class Else(AST):
	def __init__(self, token, after):
		self.token = token
		self.after = after

class Output(AST):
	def __init__(self, token, expr):
		self.token = token
		self.expr = expr

class Declarative(AST):
	def __init__(self, token, var, assigned):
		self.token = token
		self.var = var
		self.assigned = assigned

class PlusEquals(AST):
	def __init__(self, left, op, right):
		self.left = left
		self.token = self.op = op
		self.right = right

class MinusEquals(AST):
	def __init__(self, left, op, right):
		self.left = left
		self.token = self.op = op
		self.right = right

class DivEquals(AST):
	def __init__(self, left, op, right):
		self.left = left
		self.token = self.op = op
		self.right = right

class MulEquals(AST):
	def __init__(self, left, op, right):
		self.left = left
		self.token = self.op = op
		self.right = right

class LessThan(AST):
	def __init__(self, left, op, right):
		self.left = left
		self.token = self.op = op
		self.right = right
	
class LessThanEqual(AST):
	def __init__(self, left, op, right):
		self.left = left
		self.token = self.op = op
		self.right = right

class GreaterThan(AST):
	def __init__(self, left, op, right):
		self.left = left
		self.token = self.op = op
		self.right = right

class GreaterThanEqual(AST):
	def __init__(self, left, op, right):
		self.left = left
		self.token = self.op = op
		self.right = right

class EqualTo(AST):
	def __init__(self, left, op, right):
		self.left = left
		self.token = self.op = op
		self.right = right

class NotEqualTo(AST):
	def __init__(self, left, op, right):
		self.left = left
		self.token = self.op = op
		self.right = right