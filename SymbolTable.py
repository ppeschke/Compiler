from collections import OrderedDict

class SymbolTable:
	def __init__(self):
		self.tab = OrderedDict()

	def declare(self, name):
		if not self.is_declared(name):
			self.tab[name] = 0
		else:
			raise Exception('Var {var_name} is already declared.'.format(var_name=name))
	
	def declare_array(self, name, length):
		if not self.is_declared(name):
			self.tab[name] = [0]*length
		else:
			raise Exception('Var {var_name} is already declared.'.format(var_name=name))
	
	def lookup(self, var_name, index=None):
		if not self.is_declared(var_name):
			raise Exception('Variable: {name} not declared'.format(name=var_name))
		if index is not None:
			return self.tab[var_name][index]
		else:
			return self.tab[var_name]

	def is_declared(self, var_name):
		return var_name in self.tab
	
	def assign(self, name, value, index=None):
		if index is not None:
			if self.is_declared(name):
				self.tab[name][index] = value
			else:
				raise Exception('Var {var_name} is not declared.'.format(var_name=name))
		else:
			if self.is_declared(name):
				self.tab[name] = value
			else:
				raise Exception('Var {var_name} is not declared.'.format(var_name=name))
