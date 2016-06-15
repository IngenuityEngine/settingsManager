
import inspect

'''
Simple object that allows dot notation for Settings.

Takes settings in as keyword args and sets them as class
properties
'''

class Settings(object):

	def __init__(self, **kwargs):
		self.set(**kwargs)

	def set(self, **kwargs):
		for key, value in kwargs.items():
			setattr(self, key, value)

	def get(self, key):
		if hasattr(self, key):
			return getattr(self, key)
		return None

	def getAll(self):
		def propertiesOnly(func):
			return not inspect.ismethod(func)

		methods = inspect.getmembers(self, predicate=propertiesOnly)
		# ignore properties that start with underscores
		# they're likely magic properties or 'private'
		methods = [method[0] for method in methods
			if method[0][0] != '_']

		settings = {}
		for method in methods:
			settings[method] = getattr(self, method)
		return settings


def main():
	options = Settings(sup='yes', x=12)
	print options.getAll()

if __name__ == '__main__':
	main()
