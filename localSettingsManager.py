import json

from settingsInterface import SettingsInterface


class LocalSettingsManager(SettingsInterface):

	def __init__(self, rootDir):
		self.rootDir = rootDir
		self.user = ''
		self.key = ''

	def create(self, key, user=''):
		try:
			#First, check whether the key already exists
			self.load(key)
			#check whether the key has this user already associated
			if user and self.settings and user in self.settings:
				self.load(key, user)
			#If no user could be loaded, make a new user
			elif user:
				self.user = user
				self.save()
		except:
			#The key does not exist yet: make a new settings file
			self.key = key
			self.user = user
			self.settings = {'default': {}}
			if user:
				self.settings[user] = {}
			self.currentSettings = {}
			self.save()
		return self

	def load(self, key, user=''):
		#Store any information still left over from the last user
		if self.user:
			self.save()
		self.key = key
		try:
			with open(self.rootDir+ key+'.json') as f:
				self.settings = json.load(f)
			self.currentSettings = self.settings['default'].copy()
			if user:
				try:
					self.currentSettings.update(self.settings[user])

					self.user = user
				except KeyError:
					pass
			return self
		except IOError:
			raise IOError('The specified settings file does not exist, perhaps you should make one:', key, user)


	def save(self, saveAs=None):
		toSave = 'default'
		if self.user:
			toSave = self.user
		if saveAs:
			toSave = saveAs

		userSettings = self.settings.pop(toSave)
		userSettings.update(self.currentSettings)
		changedSettings = {}

		for key in userSettings:
			if toSave == 'default':
				changedSettings[key] = userSettings[key]
			elif (key not in self.settings['default'] or
				(key in self.settings['default'] and  userSettings[key] != self.settings['default'][key])):
					changedSettings[key] = userSettings[key]
		self.settings[toSave] = changedSettings
		with open(self.rootDir+self.key+'.json', 'w') as settingsFile:
			json.dump(self.settings, settingsFile, indent=4)

	def set(self, key, value=None):
		if value:
			self.currentSettings[key] = value
		else:
			self.currentSettings.update(key)

	def get(self, key=None):
		if key is None:
			return self.currentSettings
		try:
			return self.currentSettings[key]
		except:
			raise KeyError('This setting for ' + key + ' has not been defined yet!')
