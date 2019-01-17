from Interpreter import Interpreter

def main():
	while True:
		try:
			text = raw_input('calc>')
		except EOFError:
			break
		if not text:
			continue
		interpreter = Interpreter(text)
		result = interpreter.expr()
		print(result)

if __name__ == '__main__':
	main()
