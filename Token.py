class Token(object):
	def __init__(self, type, value, line_number):
		self.type = type
		self.value = value
		self.line_number = line_number
	
	def __str__(self):
		return 'Token({type}, {value}, {line})'.format(
			type=self.type,
			value = repr(self.value),
			line=self.line_number
		)
	
	def __repr__(self):
		return self.__str__()