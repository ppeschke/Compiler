from Token import Token
from Lexer import *
from Parser import Parser
from AST import AST
from SymbolTable import SymbolTable
from NodeVisitor import NodeVisitor

class CodeGenerator(NodeVisitor):
	def __init__(self, parser):
		self.symtab = SymbolTable()
		self.parser = parser
		root = self.parser.parse()
		self.visit(root)