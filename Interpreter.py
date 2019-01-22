from Token import Token
from Lexer import *
from Parser import Parser
from AST import AST
from SymbolTable import SymbolTable

class NodeVisitor(object):
	def visit(self, node):
		method_name = 'visit_' + type(node).__name__
		visitor = getattr(self, method_name, self.generic_visit)
		return visitor(node)
	
	def generic_visit(self, node):
		raise Exception('No visit_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):
	def __init__(self, parser):
		self.symtab = SymbolTable()
		self.parser = parser
		root = self.parser.parse()
		self.visit(root)
	
	def visit_BinOp(self, node):
		if node.op.type == PLUS:
			return self.visit(node.left) + self.visit(node.right)
		elif node.op.type == MINUS:
			return self.visit(node.left) - self.visit(node.right)
		elif node.op.type == MUL:
			return self.visit(node.left) * self.visit(node.right)
		elif node.op.type == DIV:
			return self.visit(node.left) // self.visit(node.right)
		elif node.op.type == MOD:
			return self.visit(node.left) % self.visit(node.right)
		
	def visit_Num(self, node):
		return node.value

	def visit_UnaryOp(self, node):
		op = node.op.type
		var = node.identifier.value
		value = self.visit(node.identifier)
		if op == INCREMENTOR:
			 value += 1
		elif op == DECREMENTOR:
			value -= 1
		self.symtab.assign(var, value)
		return var

	def visit_Compound(self, node):
		for child in node.children:
			self.visit(child)
	
	def visit_Assign(self, node):
		var_name = node.left.var_name
		value = self.visit(node.right)
		self.symtab.assign(var_name, value)

	def visit_Declarative(self, node):
		self.symtab.declare(node.var.var_name)
		if node.assigned is not None:
			self.visit(node.assigned)
	
	def visit_Var(self, node):
		return self.symtab.lookup(node.var_name)

	def visit_Output(self, node):
		value = self.visit(node.expr)
		print(value)
	
	def visit_PlusEquals(self, node):
		var_name = node.left.var_name
		value = self.symtab.lookup(var_name) + self.visit(node.right)
		self.symtab.assign(var_name, value)
	
	def visit_MinusEquals(self, node):
		var_name = node.left.var_name
		value = self.symtab.lookup(var_name) - self.visit(node.right)
		self.symtab.assign(var_name, value)

	def visit_DivEquals(self, node):
		var_name = node.left.var_name
		value = self.symtab.lookup(var_name) // self.visit(node.right)
		self.symtab.assign(var_name, value)
	
	def visit_MulEquals(self, node):
		var_name = node.left.var_name
		value = self.symtab.lookup(var_name) * self.visit(node.right)
		self.symtab.assign(var_name, value)

	def visit_ModEquals(self, node):
		var_name = node.left.var_name
		value = self.symtab.lookup(var_name) % self.visit(node.right)
		self.symtab.assign(var_name, value)
	
	def visit_Loop(self, node):
		while self.visit(node.condition):
			self.visit(node.body)
	
	def visit_Body(self, node):
		for c in node.children:
			self.visit(c)
	
	def visit_LessThan(self, node):
		return self.visit(node.left) < self.visit(node.right)
	
	def visit_LessThanEqual(self, node):
		return self.visit(node.left) <= self.visit(node.right)

	def visit_GreaterThan(self, node):
		return self.visit(node.left) > self.visit(node.right)
	
	def visit_GreaterThanEqual(self, node):
		return self.visit(node.left) >= self.visit(node.right)
	
	def visit_EqualTo(self, node):
		return self.visit(node.left) == self.visit(node.right)
	
	def visit_NotEqualTo(self, node):
		return self.visit(node.left) != self.visit(node.right)
	
	def visit_If(self, node):
		if self.visit(node.condition):
			self.visit(node.body)
		elif node.else_node is not None:
			self.visit(node.else_node)
	
	def visit_CompoundCondition(self, node):
		left = self.visit(node.left)
		if left:
			if node.op.value == '||':
				return True	#ignore right side because True or X will always be True
			else:
				return self.visit(node.right)
		else:
			if node.op.value == '&&':
				return False	#ignore right side because False and X will always be False
			else:
				return self.visit(node.right)