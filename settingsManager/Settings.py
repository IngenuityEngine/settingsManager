class Settings(object):

	def __init__(self, **kwargs):
	    for key, value in kwargs.items():
	      	setattr(self, key, value)

	def append(self, **kwargs):
		for key, value in kwargs.items():
			setattr(self, key, value)