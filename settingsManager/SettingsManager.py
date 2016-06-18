import os
import json
import types

from Settings import Settings
import arkInit
arkInit.init()

import arkUtil


class SettingsManager(Settings):

	def __init__(self, appName='default', user=None):

		# store the basics
		self.appName = appName
		self.user = user
		self.settings = {}
		self.rootDir = os.environ.get('ARK_CONFIG')

		# create the file we're trying to load
		self.filename = self.rootDir + '/' + appName + '.json'

		# load it then run setup
		# (setup currently only does anything in global settings)
		self.loadFromFile(self.filename)
		self.setup()

		# try to load additional settings based on
		# user, ark_mode, etc
		try:
			self.overrideSettings()
		except:
			pass

		# self.set(self.settings)

		# for  in self.settings:
		# 	setattr(self, key, self.get(key))

	def loadFromFile(self, filename):
		with open(filename) as f:
			settings = arkUtil.parseJSON(f)
			self.updateSettings(settings)

	def get(self, key):
		if key in self.settings:
				lookup = self.settings[key]
				return self.formatAnswer(lookup)
		else:
			raise KeyError('%s is not a setting!' % key)

	def formatAnswer(self, key):
		keyType = type(key)
		if isinstance(key, types.StringTypes):
			completedResult = key
			# fix: should use regex here
			while '{' in completedResult:
				completedResult = completedResult\
					.format(**self.settings)
			return str(completedResult)
		elif keyType == types.ListType:
			return [self.formatAnswer(x) for x in key]
		elif keyType == types.DictType:
			# return {x: self.formatAnswer(key[x]) for x in key}
			dict([(x, self.formatAnswer(key[x])) for x in key])
		else:
			return key

	def updateSettings(self, settings):
		print 'updateSettings'

		print 'self.settings:', self.settings
		print 'settings:', settings
		self.settings = arkUtil.mergeDict(self.settings, settings)

		print 'merged:', self.settings

		for key in self.settings:
			setattr(self, key, self.get(key))

	def overrideSettings(self):
		if self.user:
			# the filename is reset to the user specific files
			self.filename = self.rootDir + '/' \
				+ self.appName + '.' \
				+ self.user + '.json'

			try:
				self.loadFromFile(self.filename)
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
			filename = os.environ.get('ARK_CONFIG') + '/' \
				+ appName + '.' + user + '.json'
		else:
			filename = os.environ.get('ARK_CONFIG') + '/' \
				+ appName + '.json'

		try:
			if os.path.isdir(filename) and user:
				print('{0} already has settings for {1}!'
					.format(user, appName))
			else:
				print('{} already has default settings!'
					.format(appName))
			return SettingsManager(appName, user)
			# with open(filename) as f:
			# 	if user:
			# 		print('{0} already has settings for {1}!'
			# 			.format(user, appName))
			# 	else:
			# 		print('{} already has default settings!'
			# 			.format(appName))
			# 	return SettingsManager(appName, user)
		except:
			with open(filename, 'w') as f:
				if user:
					print('{0} just made a settings file for {1} at {2}'
						.format(user, appName, filename))
				else:
					print('Default settings were created for {}'
						.format(appName))
				f.write('{}')
				return SettingsManager(appName, user)

	def set(self, key, value=None):
		# try:
		# 	self.loadFromFile(self.filename)
		# except:
		# 	pass
		with open(self.filename, 'w+') as f:
			extraSettings = json.load(f)
			if value:
				newSettings = {key: value}
			else:
				newSettings = key
			self.updateSettings(newSettings)
			extraSettings = arkUtil.mergeDict(
				extraSettings, newSettings)
			# if value:
			# 	self.settings[key] = value
			# 	extraSettings[key] = value
			# 	setattr(self, key, self.get(key))
			# else:
			# 	self.settings.update(key)
			# 	extraSettings.update(key)
			# 	for i in key:
			# 		setattr(self, i, self.get(i))
			json.dump(extraSettings, f, indent=4, sort_keys=True)
