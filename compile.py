from Lexer import *
from Parser import Parser
from AST import AST
from Interpreter import Interpreter

def main():
	text = open('test.txt', 'r').read()
	if text:
		lexer = Lexer(text)
		parser = Parser(lexer)
		interpreter = Interpreter(parser)

if __name__ == '__main__':
	main()
