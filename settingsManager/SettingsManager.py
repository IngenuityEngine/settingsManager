import commentjson as json
from types import *
from Settings import Settings
import os



class SettingsManager(Settings):

	def __init__(self, appName=None, user=None):
		self.appName = appName
		self.user = user
		self.settings = {}
		self.rootDir = os.environ.get('ARK_CONFIG', 'c:/ie/config')
		self.pathname = self.rootDir + '/' + appName + '.json'
		self.load()
		self.setup()
		try:
			self.overrides()
		except:
			pass
		for key in self.settings:
			setattr(self, key, self.get(key))

	def load(self):
		try:
			with open(self.pathname) as f:
				self.settings = json.load(f)
		except:
			raise

	def get(self, key):
		if key in self.settings:
				lookup = self.settings[key]
				return self.formatAnswer(lookup)
		else:
			raise KeyError('%s is not a global setting!' % key)

	def formatAnswer(self, key):
		keyType = type(key)
		if isinstance(key, StringTypes):
			completedResult = key
			while '{' in completedResult:
				completedResult = completedResult.format(**self.settings)
			return str(completedResult)
		elif keyType == ListType:
			return [self.formatAnswer(x) for x in key]
		elif keyType == DictType:
			return {x: self.formatAnswer(key[x]) for x in key}
		else:
			return key

	def overrides(self):
		if self.user:
			#the pathname is reset to the user specific files
			self.pathname = self.rootDir + '/' + self.appName + '.' + self.user + '.json'
			try:
				with open(self.pathname) as f:
					extraSettings = json.load(f)
					self.settings.update(extraSettings)
					for setting in extraSettings:
						setattr(self, setting, self.get(setting))
			except:
				raise IOError('This user does not exist yet!')

	# runSetupScript is an abstract function; if a particular settings manager
	# needs to programmatically set settings it can be done here
	# settings run by runSetupScript can still be overriden by user-specific settings in
	# their config file
	def setup(self):
		pass

	@classmethod
	def create(self, appName, user=None):
		if user:
			pathname = os.environ.get('ARK_CONFIG', 'c:/ie/config') + '/' + appName + '.' + user + '.json'
		else:
			pathname = os.environ.get('ARK_CONFIG', 'c:/ie/config') + '/' + appName + '.json'
		try:
			with open(pathname) as f:
				if user:
					print('{0} already has settings for {1}!'.format(user, appName))
				else:
					print('{} already has default settings!'.format(appName))
				return SettingsManager(appName, user)
		except:
			with open(pathname, 'w') as f:
				if user:
					print('{0} just made a settings file for {1} at {2}'.format(user, appName, pathname))
				else:
					print('Default settings were created for {}'.format(appName))
				return SettingsManager(appName, user)

	def set(self, key, value=None):
		with open(self.pathname, 'w+') as f:
			extraSettings = json.load(f)
			if value:
				self.settings[key] = value
				extraSettings[key] = value
				setattr(self, key, self.get(key))
			else:
				self.settings.update(key)
				extraSettings.update(key)
				for i in key:
					setattr(self, i, self.get(i))
			json.dump(extraSettings, f, indent=4, sort_keys=True)
