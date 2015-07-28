

class SettingsInterface(object):

	def load(self, name = None):
		raise NotImplementedError

	def saveSettings(self):
		raise NotImplementedError

	def setSetting(self, key, value):
		raise NotImplementedError

	def getSetting(self, key, value):
		raise NotImplementedError

	def getSettings(self):
		raise NotImplementedError

