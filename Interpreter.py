from Token import Token, INTEGER, PLUS, MINUS, EOF
from Lexer import Lexer

class Interpreter:
	def __init__(self, parser):
		self.current_token = None
		self.parser = parser