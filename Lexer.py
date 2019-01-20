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
LBRACE = 'LBRACE'
RBRACE = 'RBRACE'
LOOP = 'LOOP'
IF = 'IF'
ELSE = 'ELSE'
OUTPUT = 'OUTPUT'
ASSIGN = 'ASSIGN'
SEMICOLON = 'SEMICOLON'
INCREMENTOR = 'INCREMENTOR'
DECREMENTOR = 'DECREMENTOR'
CONDITIONALCOMBINATOR = 'CONDITIONALCOMBINATOR'
CONDITIONALOP = 'CONDITIONALOP'
NEGATOR = 'NEGATOR'

RESERVED_WORDS = {
	'declare': DECLARE,
	'while' : LOOP,
	'if': IF,
	'else': ELSE,
	'output': OUTPUT
}

class Lexer:
	def __init__(self, text):
		self.text = text
		self.pos = 0
		self.current_char = self.text[self.pos]
		self.line = 1
		self.reserved_words = ['while', 'if', 'else', 'declare', 'output']

	def error(self):
		raise Exception('Error lexing input')

	def peek(self):
		peek_pos = self.pos + 1
		if peek_pos > len(self.text) - 1:
			return None
		else:
			return self.text[peek_pos]

	def advance(self):
		self.pos += 1
		if self.pos > len(self.text) - 1:
			self.current_char = None
		else:
			self.current_char = self.text[self.pos]
		
	def skip_whitespace(self):
		while self.current_char is not None and self.current_char.isspace():
			if self.current_char == '\n':
				self.line += 1
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
				return Token(INTEGER, self.integer(), self.line)

			if self.current_char.isalpha():
				word = self.word()
				if word in self.reserved_words:
					t = Token(IDENTIFIER, word, self.line)
					r = RESERVED_WORDS.get(word, t)
					if r == t:
						return t;
					else:
						return Token(r, word, self.line)
				else:
					t = Token(IDENTIFIER, word, self.line)
					return t

			if self.current_char == '=':
				if self.peek() == '=':
					self.advance()
					self.advance()
					return Token(CONDITIONALOP, '==')
				else:
					self.advance()
					return Token(ASSIGN, '=', self.line)
			
			if self.current_char == '<' or self.current_char == '>':
				if(self.peek() == '='):
					c = self.current_char
					self.advance()
					self.advance()
					return Token(CONDITIONALOP, c + '=', self.line)
				else:
					c = self.current_char
					self.advance()
					return Token(CONDITIONALOP, c, self.line)
			
			if self.current_char == '!':
				if(self.peek() == '='):
					self.advance()
					self.advance()
					return Token(CONDITIONALOP, '!=', self.line)
				else:
					self.advance()
					return Token(NEGATOR, '!', self.line)

			if self.current_char == '+':
				if self.peek() == '+':
					self.advance()
					self.advance()
					return Token(INCREMENTOR, '++', self.line)
				self.advance()
				return Token(PLUS, '+', self.line)
			
			if self.current_char == '-':
				if self.peek() == '-':
					self.advance()
					self.advance()
					return Token(DECREMENTOR, '--', self.line)
				self.advance()
				return Token(MINUS, '-', self.line)
			
			if self.current_char == '/':
				self.advance()
				return Token(DIV, '/', self.line)
			
			if self.current_char == '*':
				self.advance()
				return Token(MUL, '*', self.line)
			
			if self.current_char == '%':
				self.advance()
				return Token(MOD, '%', self.line)
			
			if self.current_char == ';':
				self.advance()
				return Token(SEMICOLON, ';', self.line)
			
			if self.current_char == '&' and self.peek() == '&':
				self.advance()
				self.advance()
				return Token(CONDITIONALCOMBINATOR, '&&', self.line)
			
			if self.current_char == '|' and self.peek() == '|':
				self.advance()
				self.advance()
				return Token(CONDITIONALCOMBINATOR, '||', self.line)
		
			if self.current_char == '[':
				self.advance()
				return Token(LBRACKET, '[')
			
			if self.current_char == ']':
				self.advance()
				return Token(RBRACKET, ']')
			
			if self.current_char == '{':
				self.advance()
				return Token(LBRACE, '{')
			
			if self.current_char == '}':
				self.advance()
				return Token(RBRACE, '}')

			self.error()
		
		return Token(EOF, None, self.line)