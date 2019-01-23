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
NEGATOR = 'NEGATOR'
EVALOPERATOR = 'EVALOPERATOR'
PLUSEQUALS = 'PLUSEQUALS'
MINUSEQUALS = 'MINUSEQUALS'
DIVEQUALS = 'DIVEQUALS'
MULEQUALS = 'MULEQUALS'
MODEQUALS = 'MODEQUALS'

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

	def error(self, message):
		raise Exception('Error lexing input\n' + message)

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
	
	def skip_single_line_comment(self):
		while self.current_char is not None and self.current_char != '\n':
			self.advance()
		if self.current_char is not None:
			self.line += 1;
			self.advance()
	
	def skip_multi_line_comment(self):
		while self.current_char is not None and not (self.current_char == '*' and self.peek() == '/'):
			if self.current_char == '\n':
				self.line += 1
			self.advance()
		self.advance()
		self.advance()

	def integer(self):
		result = ''
		while self.current_char is not None and self.current_char.isdigit():
			result += self.current_char
			self.advance()
		return int(result)
	
	def word(self):
		result = ''
		while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
			result += self.current_char
			self.advance()
		return result
	
	def get_next_token(self):
		while self.current_char is not None:
			if self.current_char == '/':
				if self.peek() == '/':
					self.skip_single_line_comment()
				elif self.peek() == '*':
					self.advance()
					self.advance()
					self.skip_multi_line_comment()
					continue
			
			if self.current_char.isspace():
				self.skip_whitespace()
				continue

			if self.current_char.isdigit():
				return Token(INTEGER, self.integer(), self.line)

			if self.current_char.isalpha():
				word = self.word()
				if word in self.reserved_words:
					return Token(RESERVED_WORDS.get(word), word, self.line)
				else:
					return Token(IDENTIFIER, word, self.line)

			if self.current_char == '=':
				if self.peek() == '=':
					self.advance()
					self.advance()
					return Token(EVALOPERATOR, '==', self.line)
				else:
					self.advance()
					return Token(ASSIGN, '=', self.line)
			
			if self.current_char == '<' or self.current_char == '>':
				if(self.peek() == '='):
					c = self.current_char
					self.advance()
					self.advance()
					return Token(EVALOPERATOR, c + '=', self.line)
				else:
					c = self.current_char
					self.advance()
					return Token(EVALOPERATOR, c, self.line)
			
			if self.current_char == '!':
				if(self.peek() == '='):
					self.advance()
					self.advance()
					return Token(EVALOPERATOR, '!=', self.line)
				else:
					self.advance()
					return Token(NEGATOR, '!', self.line)

			if self.current_char == '+':
				if self.peek() == '+':
					self.advance()
					self.advance()
					return Token(INCREMENTOR, '++', self.line)
				elif self.peek() == '=':
					self.advance()
					self.advance()
					return Token(PLUSEQUALS, '+=', self.line)
				self.advance()
				return Token(PLUS, '+', self.line)
			
			if self.current_char == '-':
				if self.peek() == '-':
					self.advance()
					self.advance()
					return Token(DECREMENTOR, '--', self.line)
				elif self.peek() == '=':
					self.advance()
					self.advance()
					return Token(MINUSEQUALS, '-=', self.line)
				self.advance()
				return Token(MINUS, '-', self.line)
			
			if self.current_char == '/':
				if self.peek() == '=':
					self.advance()
					self.advance()
					return Token(DIVEQUALS, '/=', self.line)
				self.advance()
				return Token(DIV, '/', self.line)
			
			if self.current_char == '*':
				if self.peek() == '=':
					self.advance()
					self.advance()
					return Token(MULEQUALS, '*=', self.line)
				self.advance()
				return Token(MUL, '*', self.line)
			
			if self.current_char == '%':
				if self.peek() == '=':
					self.advance()
					self.advance()
					return Token(MODEQUALS, '%=', self.line)
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
				return Token(LBRACKET, '[', self.line)
			
			if self.current_char == ']':
				self.advance()
				return Token(RBRACKET, ']', self.line)
			
			if self.current_char == '{':
				self.advance()
				return Token(LBRACE, '{', self.line)
			
			if self.current_char == '}':
				self.advance()
				return Token(RBRACE, '}', self.line)

			if self.current_char == '(':
				self.advance()
				return Token(LPARENT, '(', self.line)
			
			if self.current_char == ')':
				self.advance()
				return Token(RPARENT, ')', self.line)

			self.error('Unrecognized character: ' + self.current_char + ' on ' + str(self.line))
		
		return Token(EOF, None, self.line)