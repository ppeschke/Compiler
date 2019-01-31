from collections import OrderedDict
from Var import Var

class SymbolTable:
	def __init__(self):
		self.tab = OrderedDict()
		self.address = 255

	def declare(self, name):
		if not self.is_declared(name):
			self.tab[name] = Var(self.address)
			self.address -= 1
		else:
			raise Exception('Var {var_name} is already declared.'.format(var_name=name))
	
	def declare_array(self, name, length):
		if not self.is_declared(name):
			self.tab[name] = []
			self.address -= (length - 1)
			for count in range(0, length):
				self.tab[name].append(Var(self.address+count))
			self.address -= 1
		else:
			raise Exception('Var {var_name} is already declared.'.format(var_name=name))
	
	def lookup(self, var_name, index=None):
		if not self.is_declared(var_name):
			raise Exception('Variable: {name} not declared'.format(name=var_name))
		if index is not None:
			return self.tab[var_name][index]
		else:
			return self.tab[var_name]
	
	def lookup_address(self, var_name, index=None):
		if not self.is_declared(var_name):
			raise Exception('Variable: {name} not declared'.format(name=var_name));
		if index is not None:
			return self.tab[var_name][index].address
		else:
			return self.tab[var_name].address

	def is_declared(self, var_name):
		return var_name in self.tab
	
	def assign(self, name, value, index=None):
		if self.is_declared(name):
			if index is not None:
				self.tab[name][index].value = value
			else:
				self.tab[name].value = value
		else:
			raise Exception('Var {var_name} is not declared.'.format(var_name=name))
