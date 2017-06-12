import os
import json
import types

from Settings import Settings
import arkInit
arkInit.init()

import arkUtil
import cOS


class SettingsManager(Settings):

	# if True, keys will be set on the class instance
	# ex: foo=bar will be class.foo = bar
	# in this case all keys should be upper case
	# to avoid collisions
	setKeysOnClass = False

	def __init__(self, appName='default', user=None):

		# store the basics
		self.appName = appName
		self.user = user
		self.settings = {}
		self.customSettings = {}

		self.rootDir = cOS.ensureEndingSlash(
			os.environ.get('ARK_ROOT') + '/ark/config')

		# set the file we're trying to load
		self.filename = self.getFilename(appName)

		# load it then run setup
		# (setup currently only does anything
		# for global settings)
		# setup() is called before the initial load.
		# the idea is that setup is setting variables
		# that are then used when loading the
		# rest of the settings, ex: ARK_ROOT
		self.setup()
		try:
			self.updateFromFile(self.filename)
		except:
			print 'No settings exist for:', self.filename
			pass

		# try to load additional settings based on
		# user, mode, etc
		self.getUserSettings()
		self.overrideSettings()
		self.updateSettings()

		if not self.user:
			self.customSettings = self.settings

	# runSetupScript is an abstract function;
	# if a particular settings manager
	# needs to programmatically set settings
	# it can be done here
	# settings run by runSetupScript can still
	# be overriden by user-specific settings in
	# their config file
	def setup(self):
		pass

	def getFilename(self, appName, user=None):
		appName = arkUtil.makeWebSafe(appName)
		if user:
			user = arkUtil.makeWebSafe(user)
			return self.rootDir + appName + \
			'.' + user + '.json'
		else:
			return self.rootDir + appName + '.json'

	def updateFromFile(self, filename):
		with open(filename) as f:
			settings = arkUtil.parseJSON(f)
			self.updateSettings(settings)

	def get(self, key):
		if key in self.settings:
			lookup = self.settings[key]
			return self.resolveKey(lookup)
		else:
			return None

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

		if self.setKeysOnClass:
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

	def getUserSettings(self):
		if not self.user:
			return

		for f in [f for f in os.listdir(os.environ['ARK_CONFIG']) if os.path.isfile(f)]:
			self.filename = os.environ['ARK_CONFIG'] + '/' + f
			try:
				self.updateFromFile(self.filename)
			except:
				pass

	def set(self, key, value=None):
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
		self.customSettings = arkUtil.mergeDict(
				self.customSettings, newSettings
			)

		return self

	def save(self):
		with open(self.filename, 'w+') as f:
			# can error if the settings file doesn't
			# exist yet
			try:
				existingSettings = arkUtil.parseJSON(f)
			except:
				existingSettings = {}

			existingSettings = arkUtil.mergeDict(
				existingSettings, self.customSettings)

			json.dump(existingSettings,
				f,
				indent=4,
				sort_keys=True)
