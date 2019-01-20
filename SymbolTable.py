class SymbolTable:
	def __init__(self):
		self.tab = {}

	def declare(self, name):
		if not self.is_declared(name):
			self.tab[name] = 0
		else:
			raise Exception('Var {var_name} is already declared.'.format(var_name=name))
	
	def lookup(self, var_name):
		if not self.is_declared(var_name):
			raise Exception('Variable: {name} not declared'.format(name=var_name))
		return self.tab[var_name]

	def is_declared(self, var_name):
		value = self.tab.get(var_name, None)
		if value == None:
			return False
		return True
	
	def assign(self, name, value):
		if self.is_declared(name):
			self.tab[name] = value
		else:
			raise Exception('Var {var_name} is not declared.'.format(var_name=name))
