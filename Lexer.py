from Token import Token
INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'
MOD = 'MOD'
EOF = 'EOF'
DECLARE = 'DECLARE'
IDENTIFIER = 'IDENTIFIER'
LBRACKET = 'LBRACKET'
RBRACKET = 'RBRACKET'
LPARENT = 'LPARENT'
RPARENT = 'RPARENT'
LOOP = 'LOOP'
IF = 'IF'
ELSE = 'ELSE'
OUTPUT = 'OUTPUT'
ASSIGN = 'ASSIGN'
SEMICOLON = 'SEMICOLON'
INCREMENTOR = 'INCREMENTOR'
DECREMENTOR = 'DECREMENTOR'
CONDITIONALAND = 'CONITIONALAND'
CONDITIONALOR = 'CONDITIONALOR'

RESERVED_WORDS = {
	'declare': Token(DECLARE, 'declare'),
	'while': Token(LOOP, 'while'),
	'if': Token(IF, 'if'),
	'else': Token(ELSE, 'else')
}

class Lexer:
	def __init__(self, text):
		self.text = text
		self.pos = 0
		self.current_char = self.text[self.pos]
		self.reserved_words = ['while', 'if', 'else', 'declare']

	def error(self):
		raise Exception('Error lexing input')

	def advance(self):
		self.pos += 1
		if self.pos > len(self.text) - 1:
			self.current_char = None
		else:
			self.current_char = self.text[self.pos]
		
	def skip_whitespace(self):
		while self.current_char is not None and self.current_char.isspace():
			self.advance()

	def integer(self):
		result = ''
		while self.current_char is not None and self.current_char.isdigit():
			result += self.current_char
			self.advance()
		return int(result)
	
	def word(self):
		result = ''
		while self.current_char is not None and self.current_char.isalnum():
			result += self.current_char
			self.advance()
		return result
	
	def get_next_token(self):
		while self.current_char is not None:
			if self.current_char.isspace():
				self.skip_whitespace()

			if self.current_char.isdigit():
				return Token(INTEGER, self.integer())

			if self.current_char.isalpha():
				word = self.word()
				if word in self.reserved_words:
					return RESERVED_WORDS.get(word, Token(IDENTIFIER, word))
				else:
					return Token(IDENTIFIER, word)
			
			if self.current_char == '+':
				self.advance()
				return Token(PLUS, '+')
			
			if self.current_char == '-':
				self.advance()
				return Token(MINUS, '-')
			
			if self.current_char == '/':
				self.advance()
				return Token(DIV, '/')
			
			if self.current_char == '*':
				self.advance()
				return Token(MUL, '*')
			
			if self.current_char == '%':
				self.advance()
				return Token(MOD, '%')
			
			if self.current_char == ';':
				self.advance()
				return Token(SEMICOLON, ';')
			
			if self.current_char == '=':
				self.advance()
				return Token(ASSIGN, '=')
		
			self.error()
		
		return Token(EOF, None)