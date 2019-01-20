from Token import Token
from Lexer import *
from AST import *

class Parser:
	def __init__(self, lexer):
		self.current_token = None
		self.lexer = lexer
	
	def error(self, t):
		raise Exception('Parser Error: Unexpected token {token_type}'.format(token_type=t))

	def eat(self, token_type):
		if self.current_token.type == token_type:
			self.current_token = self.lexer.get_next_token()
		else:
			self.error(self.current_token.type)

	def output(self):
		#output         : out expression
		token = self.current_token
		self.eat(OUTPUT)
		expr = self.expression()
		self.eat(SEMICOLON)
		return Output(token, expr)

	def doelse(self):
		#else           : ELSE (if|body)
		token = self.current_token
		self.eat(ELSE)
		if self.current_token.type == IF:
			after = self.doif()
		else:
			after = self.body()
		return Else(token, after)

	def doif(self):
		#if             : IF LPARENT condition RPARENT body else*
		token = self.current_token
		self.eat(LPARENT)
		cond = self.condition()
		self.eat(RPARENT)
		bod = self.body()
		else_node = None
		if self.current_token.type == ELSE:
			else_node = self.doelse()
		return If(cond, bod, else_node)


	def body(self):
		#body           : (LBRACE statement(statement)* RBRACE | statement )
		if self.current_token.type == LBRACE:
			self.eat(LBRACE)
			while self.current_token.type != RBRACE:
				self.statement()
				self.eat(RBRACE)
		else:
			self.statement()

	def evaloperator(self):
		#evaloperator   : (<|>|<=|>=|==|!=)
		self.eat(EVALOPERATOR)
		return 

	def condition(self):
		#condition      : LPARENT condition RPARENT | factor | factor evaloperator factor | condition (AND | OR) condition
		if self.current_token.type == LPARENT:
			self.eat(LPARENT)
			cond = self.condition()
			self.eat(RPARENT)
		else:	#simple condition
			left = self.factor()
			if self.current_token.type == RPARENT or self.current_token.type == CONDITIONALCOMBINATOR:
				op = Token(EVALOPERATOR, '==')
				right = Token(INTEGER, 0)
			else:
				op = self.evaloperator()
				right = self.factor()
			cond = Condition(left, op, right)
		
		if self.current_token.type == CONDITIONALCOMBINATOR:
			left = cond
			op = self.current_token
			self.eat(CONDITIONALCOMBINATOR)
			right = self.condition()
			return Condition(left, op, right)
		elif self.current_token.type == RPARENT:
			return cond
		else:
			self.error(self.current_token.type)

	def loop(self):
		#loop           : while LPARENT condition RPARENT body
		token = self.current_token
		self.eat(WHILE)
		self.eat(LPARENT)
		condition = self.confition()
		self.eat(RPARENT)
		body = self.body()
		return Loop(token, condition, body)

	def decrementor(self):
		#decrementor    : --IDENTIFIER
		token = self.current_token
		self.eat(DECREMENTOR)
		return UnaryOp(token, self.identifier())

	def incrementor(self):
		#incrementor    : ++IDENTIFIER
		token = self.current_token
		self.eat(INCREMENTOR)
		return UnaryOp(token, self.identifier())
	
	def factor(self):
		#factor         : (LPARENT expression RPARENT|INTEGER|IDENTIFIER|incrementor|decrementor)
		if self.current_token.type == LPARENT:
			self.eat(LPARENT)
			node = self.expression()
			self.eat(RPARENT)
			return node
		elif self.current_token.type == INTEGER:
			token = self.current_token
			self.eat(INTEGER)
			return Num(token)
		elif self.current_token.type == IDENTIFIER:
			return self.identifier()
		elif self.current_token.type == INCREMENTOR:
			return self.incrementor()
		elif self.current_token.type == DECREMENTOR:
			return self.decrementor()

	def term(self):
		#term           : factor ((MUL|DIV|MOD) factor)+
		node = self.factor()
		while self.current_token in (MUL, DIV, MOD):
			token = self.current_token
			if token.type == MUL:
				self.eat(MUL)
			elif token.type == DIV:
				self.eat(DIV)
			elif token.type == MOD:
				self.eat(MOD)
			node = BinOp(left=node, op=token, right=self.factor())
		return node

	def expression(self):
		#expression     : term ((PLUS|MINUS)term)+
		node = self.term()
		while self.current_token.type in (PLUS, MINUS):
			token = self.current_token
			if token.type == PLUS:
				self.eat(PLUS)
			elif token.type == MINUS:
				self.eat(MINUS)
			node = BinOp(left=node, op=token, right=self.term())
		return node
	
	def assignment(self):
		#assignment     : IDENTIFIER = expression SEMICOLON
		left = self.identifier()
		op = self.current_token
		self.eat(ASSIGN)
		right = self.expression()
		self.eat(SEMICOLON)
		return Assign(left, op, right)

	def identifier(self):
		#IDENTIFIER     : [_a-zA-Z][_a-zA-Z0-9] (indexer)+
		token = self.current_token
		self.eat(IDENTIFIER)
		if self.current_token.type == LBRACE:
			index = self.indexer()
		else:
			index = None
		node = Var(token, index)
		return node

	def indexer(self):
		#indexer        : LBRACKET IDENTIFIER RBRACKET
		self.eat(LBRACE)
		node = self.identifier()
		self.eat(RBRACE)
		return node

	def declarative(self):
		#declarative    : DECLARE IDENTIFIER (ASSIGN exprpession) SEMICOLON
		decl_token = self.current_token
		self.eat(DECLARE)
		ident = self.identifier()
		assigned = None
		if self.current_token.type == ASSIGN:
			assign_token = self.current_token
			self.eat(ASSIGN)
			right = self.expression()
			assigned = Assign(ident, assign_token, right)
		self.eat(SEMICOLON)
		node = Declarative(decl_token, ident, assigned)
		return node

	def statement(self):
		#statement      : (declarative|assignment|loop|if|output|INCREMENTOR|DECREMENTOR)
		if self.current_token.type == DECLARE:
			node = self.declarative()
		elif self.current_token.type == IDENTIFIER:
			node = self.assignment()
		elif self.current_token.type == LOOP:
			node = self.loop()
		elif self.current_token.type == IF:
			node = self.doif()
		elif self.current_token.type == OUTPUT:
			node = self.output()
		elif self.current_token.type == INCREMENTOR:
			node = self.incrementor()
			self.eat(SEMICOLON)
		elif self.current_token.type == DECREMENTOR:
			node = self.decrementor()
			self.eat(SEMICOLON)
		else:
			self.error(self.current_token.type)
		
		return node

	def program(self):
		#program        : statement (statement)*
		self.current_token = self.lexer.get_next_token()
		node = Compound()
		while self.current_token.type != EOF:
			node.children.append(self.statement())
		return node
	
	def parse(self):
		return self.program()