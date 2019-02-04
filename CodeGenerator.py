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
		child_commands = []
		length = 0
		for c in node.children:
			commands = self.visit(c)
			length = len(child_commands)
			for command in commands:
				if command.data_type == 'dynamic':
					command.data += length
			child_commands.extend(commands)
		return child_commands
		
	def visit_Declarative(self, node):
		commands = []
		if node.var.index is not None:
			self.symtab.declare_array(node.var.var_name, self.visit(node.var.index))
		else:
			self.symtab.declare(node.var.var_name)
			if node.assigned is not None:
				commands.extend(self.visit(node.assigned))
		return commands
	
	def visit_Assign(self, node):
		#this could be an address or
		# instructions to calculate an address
		var_address = self.visit(node.left)

		if len(var_address) == 1:
			#not an array
			if type(node.right).__name__ == 'Num':
				#store number in variable
				value = self.visit(node.right)
				commands = [Command('LDI', 'instruction')]
				commands.append(Command(value, 'data'))
				commands.append(Command('STO', 'instruction'))
				commands.extend(var_address)
			else:
				#store expression result in variable
				commands = self.visit(node.right)
				commands.append(Command('STO', 'instruction'))
				commands.extend(var_address)
		else:
			#dealing with an array
			if type(node.right).__name__ == 'Num':
				#store number in array spot
				value = self.visit(node.right)
				length = len(var_address) + 4
				commands = var_address
				commands.append(Command('STO', 'instruction'))
				commands.append(Command(length + 1, 'dynamic'))
				commands.append(Command('LDI', 'instruction'))
				commands.append(Command(value, 'data'))
				commands.append(Command('STO', 'instruction'))
				commands.append(Command('0', 'dynamically filled'))
			elif type(node.right).__name__ == 'Var':
				#store var in array spot
				length = len(var_address) + 4
				right_var_address = self.visit(node.right)
				commands = var_address
				commands.append(Command('STO', 'instruction'))
				commands.append(Command(length + 1, 'dynamic'))
				commands.append(Command('LDA', 'instruction'))
				commands.extend(right_var_address)
				commands.append(Command('STO', 'instruction'))
				commands.append(Command(0, 'dynamically filled'))
			else:
				#store expression result in array spot
				length = len(var_address) + 2
				right_commands = self.visit(node.right)
				right_length = len(right_commands)
				commands = var_address
				commands.append(Command('STO', 'instruction'))
				commands.append(Command(length + right_length + 1, 'dynamic'))
				commands.extend(right_commands)
				commands.append(Command('STO', 'instruction'))
				commands.append(Command(0, 'dynamically filled'))

		return commands
	
	def visit_Var(self, node):
		if node.index is not None:
			#with index
			if type(node.index).__name__ == 'Num':
				#with numeric index
				index = self.visit(node.index)
				address = self.symtab.lookup_address(node.var_name, index)
				return [Command(address, 'address')]
			else:
				if type(node.index).__name__ == 'Var':
					#with variable index
					commands = [Command('LDA', 'instruction')]
					commands.extend(self.visit(node.index))
				else:
					#with expression index
					commands = self.visit(node.index)
				var_address = self.symtab.lookup_address(node.var_name, 0)
				commands.append(Command('ADI', 'instruction'))
				commands.append(Command(var_address, 'address'))
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
		elif type(node.expr).__name__ == 'Var':
			address = self.visit(node.expr)
			if len(address) == 1:
				commands = [Command('LDA', 'instruction')]
				commands.extend(address)
			else:
				commands = address
				commands.append(Command('STO', 'instruction'))
				commands.append(Command(len(address) + 2, 'dynamic'))
				commands.append(Command('LDI', 'instruction'))
				commands.append(Command(0, 'dynamically filled'))
		else:
			commands = self.visit(node.expr)
		commands.append(Command('OUT', 'instruction'))
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
			right_commands.extend(right_address)
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
	
	def visit_Loop(self, node):
		commands = self.visit(node.condition)
		length = len(commands)
		commands.extend(self.visit(node.body))
		commands.append(Command('JMP', 'instruction'))
		commands.append(Command(0, 'data'))	# we'll change the type later
		full_length = len(commands)
		for command in commands:
			if command.data_type == 'dynamic':
				command.data += length
			elif command.data_type == 'after loop':
				command.data = full_length
				command.data_type = 'dynamic'
		commands[-1].data_type = 'dynamic'
		return commands
	
	def visit_LessThan(self, node):
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
			if not self.symtab.is_declared('compare_left'):
				self.symtab.declare('compare_left')
			left_address = self.symtab.lookup_address('compare_left')
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
			right_commands.extend(right_address)
		else:
			immediate = False
			right_setup = self.visit(node.right)
			if not self.symtab.is_declared('compare_right'):
				self.symtab.declare('compare_right')
			right_address = self.symtab.lookup_address('compare_right')
			right_setup.append(Command('STO', 'instruction'))
			right_setup.append(Command(right_address, 'address'))
			right_commands.append(Command(right_address, 'address'))
		
		if immediate:
			operations.append(Command('SBI', 'instruction'))
		else:
			operations.append(Command('SUB', 'instruction'))
		
		commands = left_setup
		commands.extend(right_setup)
		commands.extend(left_commands)
		commands.extend(operations)
		commands.extend(right_commands)
		commands.append(Command('JC', 'instruction'))
		commands.append(Command(0, 'after loop'))
		return commands

	def visit_GreaterThan(self, node):
		left_setup = []
		left_commands = []
		right_setup = []
		right_commands = []
		operations = []
		if type(node.left).__name__ == 'Num':
			immediate = True;
			value = self.visit(node.left)
			left_commands.append(Command(value, 'data'))
		elif type(node.left).__name__ == 'Var':
			immediate = False
			left_address = self.visit(node.left)
			left_commands.extend(left_address)
		else:
			immediate = False
			if not self.symtab.is_declared('compare_left'):
				self.symtab.declare('compare_left')
			left_address = self.symtab.lookup_address('compare_left')
			left_setup = self.visit(node.left)
			#do I really need to do this? Perhaps it will be caught by the optimizer
			left_setup.append(Command('STO', 'instruction'))
			left_setup.append(Command(left_address, 'address'))
			left_commands.append(Command('LDA', 'instruction'))
			left_commands.append(Command(left_address, 'variable'))

		if type(node.right).__name__ == 'Num':
			value = self.visit(node.right)
			right_commands = [Command('LDI', 'instruction')]
			right_commands.append(Command(value, 'data'))
		elif type(node.right).__name__ == 'Var':
			right_address = self.visit(node.right)
			right_commands.append(Command('LDA', 'instruction'))
			right_commands.extend(right_address)
		else:
			right_setup = self.visit(node.right)
			if not self.symtab.is_declared('compare_right'):
				self.symtab.declare('compare_right')
			right_address = self.symtab.lookup_address('compare_right')
			right_setup.append(Command('STO', 'instruction'))
			right_setup.append(Command(right_address, 'address'))
			right_commands.append(Command(right_address, 'address'))
		
		if immediate:
			operations.append(Command('SBI', 'instruction'))
		else:
			operations.append(Command('SUB', 'instruction'))
		
		commands = right_setup
		commands.extend(left_setup)
		commands.extend(right_commands)
		commands.extend(operations)
		commands.extend(left_commands)
		commands.append(Command('JC', 'instruction'))
		commands.append(Command(0, 'after loop'))
		return commands