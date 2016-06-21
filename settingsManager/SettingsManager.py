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

		# set the file we're trying to load
		self.filename = self.getFilename(appName)

		# load it then run setup
		# (setup currently only does anything
		# for global settings)
		self.updateFromFile(self.filename)
		self.setup()

		# try to load additional settings based on
		# user, ark_mode, etc
		self.overrideSettings()
		self.updateSettings()

		# self.set(self.settings)

		# for  in self.settings:
		# 	setattr(self, key, self.get(key))

	def getFilename(self, appName, user=None):
		appName = arkUtil.makeWebSafe(appName)
		if user:
			user = arkUtil.makeWebSafe(user)
			return self.rootDir + '/' + appName + \
			'.' + user + '.json'
		else:
			return self.rootDir + '/' + appName + '.json'

	def updateFromFile(self, filename):
		with open(filename) as f:
			settings = arkUtil.parseJSON(f)
			self.updateSettings(settings)

	def get(self, key):
		if key in self.settings:
				lookup = self.settings[key]
				return self.resolveKey(lookup)
		else:
			raise KeyError('%s is not a setting!' % key)

	def resolveKey(self, key):
		keyType = type(key)
		if isinstance(key, types.StringTypes):
			completedResult = key
			# fix: should use regex here
			while '{' in completedResult:
				completedResult = completedResult\
					.format(**self.settings)
			return str(completedResult)
		elif keyType == types.ListType:
			return [self.resolveKey(x) for x in key]
		elif keyType == types.DictType:
			# return {x: self.resolveKey(key[x]) for x in key}
			return dict([(x, self.resolveKey(key[x])) for x in key])
		else:
			return key

	def updateSettings(self, settings=None):
		if settings is not None:
			self.settings = arkUtil\
				.mergeDict(self.settings, settings)

		for key in self.settings:
			setattr(self, key, self.get(key))

	def overrideSettings(self):
		# bail if we don't have a user
		# as there's nothing else to load
		if not self.user:
			return

		# the filename is reset to the user specific files
		self.filename = self.rootDir + '/' \
			+ self.appName + '.' \
			+ self.user + '.json'

		try:
			self.updateFromFile(self.filename)
		except:
			pass
			# raise IOError('This user does not exist yet!')

	# runSetupScript is an abstract function;
	# if a particular settings manager
	# needs to programmatically set settings
	# it can be done here
	# settings run by runSetupScript can still
	# be overriden by user-specific settings in
	# their config file
	def setup(self):
		pass

	def set(self, key, value=None):
		with open(self.filename, 'w+') as f:
			# can error if the settings file doesn't
			# exist yet
			try:
				existingSettings = arkUtil.parseJSON(f)
			except:
				existingSettings = {}

			# if we have key value, make a new dict
			if value is not None:
				newSettings = {key: value}
			# otherwise hopefully we passed a dict
			elif type(key) == dict:
				newSettings = key
			else:
				raise Exception('SettingsManager.set:' +
					' Invalid data')

			self.updateSettings(newSettings)
			existingSettings = arkUtil.mergeDict(
				existingSettings, newSettings)

			json.dump(existingSettings,
				f,
				indent=4,
				sort_keys=True)
