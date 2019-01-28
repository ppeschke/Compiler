from Token import Token
from Lexer import *
from Parser import Parser
from AST import AST
from SymbolTable import SymbolTable
from NodeVisitor import NodeVisitor
from Command import Command

class CodeGenerator(NodeVisitor):
	def __init__(self, parser):
		self.symtab = SymbolTable()
		self.parser = parser
		self.root = self.parser.parse()
	
	def generate(self):
		commands = self.visit(self.root)
		commands.append(Command('HLT'))
		return commands
	
	def visit_Compound(self, node):
		commands = []
		for c in node.children:
			com = self.visit(c)
			if com != []:
				commands.extend(com)
		return commands
		
	def visit_Declarative(self, node):
		if node.var.index is not None:
			self.symtab.declare(node.var.var_name, self.visit(node.var.index))
		else:
			self.symtab.declare(node.var.var_name)
			if node.assigned is not None:
				self.visit(node.assigned)
		return []
	
	def visit_Assign(self, node):
		var_address = self.visit(node.left)
		if type(node.right).__name__ == 'Num':
			value = self.visit(node.right)
			commands = [Command('LDI')]
			commands.append(Command(value))
			commands.append(Command('STO'))
			commands.extend(var_address)
		else:
			commands = self.visit(node.right)
			commands.append(Command('STO'))
			commands.extend(Command(var_address))
		return commands
	
	def visit_Var(self, node):
		if node.index is not None:
			if type(node.index).__name__ == 'Num':
				return [Command(self.visit(node.index))]
			else:
				commands = self.visit(node.index)
				var_address = self.symtab.lookup(node.var_name, 0)
				commands.append(Command('STO'))
				commands.append(Command(100))
				return commands
		else:
			commands = [Command(self.symtab.lookup(node.var_name).address)]
			return commands
	
	def visit_Num(self, node):
		return node.value

	def visit_Output(self, node):
		if type(node.expr).__name__ == 'Num':
			value = self.visit(node.expr)
			commands = [Command('LDI')]
			commands.append(Command(value))
			commands.append(Command('OUT'))
		elif type(node.expr).__name__ == 'Var':
			address = self.visit(node.expr)
			commands = [Command('LDA')]
			commands.extend(address)
			commands.append(Command('OUT'))
		else:
			commands = self.visit(node.expr)
			commands.append('OUT')
		return commands