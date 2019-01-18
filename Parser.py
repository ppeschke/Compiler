from Token import Token
from Lexer import *

class Parser:
	def __init__(self, lexer):
		self.current_token = None
		self.lexer = lexer
	
	def error(self):
		raise Exception('Error parsing input!')

	def eat(self, token_type):
		if self.current_token.type == token_type:
			self.current_token = self.lexer.get_next_token()
		else:
			self.error()

	def output(self):
		#output         : out expression
		self.eat(OUTPUT)
		self.expression()

	def doelse(self):
		#else           : ELSE (if|body)
		self.eat(ELSE)
		if self.current_token.type == IF:
			self.doif()
		else:
			self.body()

	def doif(self):
		#if             : IF LPARENT condition RPARENT body else*
		self.eat(LPARENT)
		self.condition()
		self.eat(RPARENT)
		self.body()
		if self.current_token.type == ELSE:
			self.doelse()


	def body(self):
		#body           : (LBRACKET statement(statement)* RBRACKET | statement )
		if self.current_token.type == LBRACKET:
			self.eat(LBRACKET)
			while self.current_token.type != RBRACKET:
				self.statement()
				self.eat(RBRACKET)
		else:
			self.statement()

	def evaloperator(self):
		#evaloperator   : (<|>|<=|>=|==|!=)
		self.eat(EVALOPERATOR)

	def condition(self):
		#condition      : value evaloperator value ((&& | ||) condition)
		self.value()
		self.evaloperator()
		self.value()
		if self.current_token.type == CONDITIONALAND:
			self.eat(CONDITIONALAND)
			self.condition()
		elif self.current_token.type == CONDITIONALOR:
			self.eat(CONDITIONALOR)
			self.condition()


	def loop(self):
		#loop           : while LPARENT condition RPARENT body
		self.eat(WHILE)
		self.eat(LPARENT)
		self.confition()
		self.eat(RPARENT)
		self.body()

	def decrementor(self):
		#decrementor    : --IDENTIFIER
		self.eat(DECREMENTOR)
		self.identifier()

	def incrementor(self):
		#incrementor    : ++IDENTIFIER
		self.eat(INCREMENTOR)
		self.identifier()

	def term(self):
		#term           : value ((MUL|DIV|MOD) value)+
		self.value()
		while self.current_token in (MUL, DIV, MOD):
			if self.current_token.type == MUL:
				self.eat(MUL)
				self.term()
			elif self.current_token.type == DIV:
				self.eat(DIV)
				self.term()
			elif self.current_token.type == MOD:
				self.eat(MOD)
				self.term()

	def expression(self):
		#expression     : term ((PLUS|MINUS)term)+
		self.term()
		while self.current_token.type in (PLUS, MINUS):
			token = self.current_token
			if token.type == PLUS:
				self.eat(PLUS)
				self.term()
			elif token.type == MINUS:
				self.eat(MINUS)
				self.term()
	
	def assignment(self):
		#assignment     : IDENTIFIER = expression SEMICOLON
		self.identifier()
		self.eat(ASSIGN)
		self.expression()
		self.eat(SEMICOLON)

	def value(self):
		#value          : (LPARENT expression RPARENT|INTEGER|IDENTIFIER|incrementor|decrementor)
		if self.current_token.type == LPARENT:
			self.eat(LPARENT)
			self.expression()
			self.eat(RPARENT)
		elif self.current_token.type == INTEGER:
			print('Integer found: ', self.current_token.value)
			self.eat(INTEGER)
		elif self.current_token.type == IDENTIFIER:
			self.identifier()
		elif self.current_token.type == INCREMENTOR:
			self.incrementor()
		elif self.current_token.type == DECREMENTOR:
			self.decrementor()

	def identifier(self):
		#IDENTIFIER     : [_a-zA-Z][_a-zA-Z0-9] (indexer)+
		print('identifier found: ', self.current_token.value)
		self.eat(IDENTIFIER)
		if self.current_token.type == LBRACKET:
			self.indexer()

	def indexer(self):
		#indexer        : LBRACKET IDENTIFIER RBRACKET
		self.eat(LBRACKET)
		self.identifier()
		self.eat(RBRACKET)

	def declarative(self):
		#declarative    : DECLARE IDENTIFIER (ASSIGN exprpession) SEMICOLON
		self.eat(DECLARE)
		self.identifier()
		if self.current_token.type == ASSIGN:
			self.eat(ASSIGN)
			self.expression()
		self.eat(SEMICOLON)

	def statement(self):
		#statement      : (declarative|assignment|loop|if|output)
		if self.current_token.type == DECLARE:
			self.declarative()
		elif self.current_token.type == IDENTIFIER:
			self.assignment()
		elif self.current_token.type == LOOP:
			self.loop()
		elif self.current_token.type == IF:
			self.doif()
		elif self.current_token.type == OUTPUT:
			self.output()
		else:
			self.error()

	def program(self):
		#program        : statement (statement)*
		self.current_token = self.lexer.get_next_token()
		while self.current_token.type != EOF:
			print('In program, current_token.type=', self.current_token.type)
			self.statement()