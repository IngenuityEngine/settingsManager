from localSettingsManager import LocalSettingsManager
from databaseSettingsManager import DatabaseSettingsManager
from settingsInterface import SettingsInterface

class SettingsManager(SettingsInterface):

	def __init__(self, backer, options):
		if backer == 'local':
			self.settingsManager = LocalSettingsManager(options)
		elif backer == 'database':
			self.settingsManager = DatabaseSettingsManager(options)
		else:
			pass

	def create(self, key, name=None):
		if not self.settingsManager:
			raise NotImplementedError
		else:
			return self.settingsManager.create(key, name)

	def load(self, key, name = None):
		if not self.settingsManager:
			raise NotImplementedError
		else:
			return self.settingsManager.load(key, name)

	def save(self, saveAs=None):
		if not self.settingsManager:
			raise NotImplementedError
		else:
			return self.settingsManager.save()

	def set(self, key, value = None):
		if not self.settingsManager:
			raise NotImplementedError
		else:
			return self.settingsManager.set(key, value)


	def get(self, key=None):
		if not self.settingsManager:
			raise NotImplementedError
		else:
			return self.settingsManager.get(key)

