from Lexer import *
from Parser import Parser

def main():
	text = open('test.txt', 'r').read()
	if text:
		lexer = Lexer(text)
		parser = Parser(lexer)
		parser.program()

if __name__ == '__main__':
	main()
