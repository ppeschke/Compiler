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
		commands.append(Command('HLT', 'instruction'))
		return commands
	
	def visit_Compound(self, node):
		commands = []
		for c in node.children:
			com = self.visit(c)
			if com != []:
				commands.extend(com)
		return commands
		
	def visit_Declarative(self, node):
		commands = []
		if node.var.index is not None:
			self.symtab.declare(node.var.var_name, self.visit(node.var.index))
		else:
			self.symtab.declare(node.var.var_name)
			if node.assigned is not None:
				commands.extend(self.visit(node.assigned))
		return commands
	
	def visit_Assign(self, node):
		var_address = self.visit(node.left)
		if type(node.right).__name__ == 'Num':
			value = self.visit(node.right)
			commands = [Command('LDI', 'instruction')]
			commands.append(Command(value, 'data'))
			commands.append(Command('STO', 'instruction'))
			commands.extend(var_address)
		else:
			commands = self.visit(node.right)
			commands.append(Command('STO', 'instruction'))
			commands.extend(var_address)
		return commands
	
	def visit_Var(self, node):
		if node.index is not None:
			if type(node.index).__name__ == 'Num':
				return [Command(self.visit(node.index), 'data')]
			else:
				commands = self.visit(node.index)
				var_address = self.symtab.lookup(node.var_name, 0)
				commands.append(Command('STO', 'instruction'))
				commands.append(Command(4, 'variable'))
				return commands
		else:
			commands = [Command(self.symtab.lookup(node.var_name).address, 'variable')]
			return commands
	
	def visit_Num(self, node):
		return node.value

	def visit_Output(self, node):
		if type(node.expr).__name__ == 'Num':
			value = self.visit(node.expr)
			commands = [Command('LDI', 'instruction')]
			commands.append(Command(value, 'data'))
			commands.append(Command('OUT', 'instruction'))
		elif type(node.expr).__name__ == 'Var':
			address = self.visit(node.expr)
			commands = [Command('LDA', 'instruction')]
			commands.extend(address)
			commands.append(Command('OUT', 'instruction'))
		else:
			commands = self.visit(node.expr)
			commands.append('OUT', 'instruction')
		return commands
	
	def visit_BinOp(self, node):
		left_setup = []
		left_commands = []
		right_setup = []
		right_commands = []
		operations = []
		if type(node.left).__name__ == 'Num':
			value = self.visit(node.left)
			left_commands = [Command('LDI', 'instruction')]
			left_commands.append(Command(value, 'data'))
		elif type(node.left).__name__ == 'Var':
			immediate = False
			left_address = self.visit(node.left)
			left_commands.append(Command('LDA', 'instruction'))
			left_commands.extend(left_address)
		else:
			if not self.symtab.is_declared('binop_left'):
				self.symtab.declare('binop_left')
			left_address = self.symtab.lookup_address('binop_left')
			left_setup = self.visit(node.left)
			#do I really need to do this? Perhaps it will be caught by the optimizer
			left_setup.append(Command('STO', 'instruction'))
			left_setup.append(Command(left_address, 'address'))
			left_commands.append(Command('LDA', 'instruction'))
			left_commands.append(Command(left_address, 'variable'))

		if type(node.right).__name__ == 'Num':
			immediate = True;
			value = self.visit(node.right)
			right_commands.append(Command(value, 'data'))
		elif type(node.right).__name__ == 'Var':
			immediate = False
			right_address = self.visit(node.right)
			right_commands.append(Command(right_address, 'variable'))
		else:
			immediate = False
			right_setup = self.visit(node.right)
			if not self.symtab.is_declared('binop_right'):
				self.symtab.declare('binop_right')
			right_address = self.symtab.lookup_address('binop_right')
			right_setup.append(Command('STO', 'instruction'))
			right_setup.append(Command(right_address, 'address'))
			right_commands.append(Command(right_address, 'address'))
			
		if node.op.value == '+':
			if immediate:
				operations.append(Command('ADI', 'instruction'))
			else:
				operations.append(Command('ADD', 'instruction'))
		elif node.op.value == '-':
			if immediate:
				operations.append(Command('SBI', 'instruction'))
			else:
				operations.append(Command('SUB', 'instruction'))
		elif node.op.value == '*':
			#do something here
			raise Exception('multiplication not implemented yet!')
		elif node.op.value == '/':
			#do something here
			raise Exception('division not implemented yet!')
		elif node.op.value == '%':
			#do something here
			raise Exception('modulus not implemented yet!')
		commands = left_setup
		commands.extend(right_setup)
		commands.extend(left_commands)
		commands.extend(operations)
		commands.extend(right_commands)
		return commands