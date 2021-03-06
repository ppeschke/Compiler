from Lexer import *
from Parser import Parser
from AST import AST
from CodeGenerator import CodeGenerator
import sys

def main():
	if len(sys.argv) == 2:
		text = open(sys.argv[1], 'r').read()
	else:
		text = open('test.txt', 'r').read()
	if text:
		lexer = Lexer(text)
		parser = Parser(lexer)
		codeGen = CodeGenerator(parser)
		commands = codeGen.generate()
		f = open('a.txt', 'w')
		for command in commands:
			f.write(str(command.data) + '\n')
		f.close()

if __name__ == '__main__':
	main()
