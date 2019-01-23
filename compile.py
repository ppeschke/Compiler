from Lexer import *
from Parser import Parser
from AST import AST
from CodeGenerator import CodeGenerator

def main():
	text = open('test.txt', 'r').read()
	if text:
		lexer = Lexer(text)
		parser = Parser(lexer)
		codeGen = CodeGenerator(parser)

if __name__ == '__main__':
	main()
