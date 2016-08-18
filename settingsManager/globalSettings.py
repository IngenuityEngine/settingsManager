import os
import sys

from SettingsManager import SettingsManager
import arkInit
arkInit.init()
import cOS
import arkUtil

class globalSettings(SettingsManager):

	nodeTypes = ['render']
	setKeysOnClass = True

	def __init__(self):
		self.MODE = os.environ.get('mode', 'default')
		# Note: Linux is case sensitive, so we cannot lower the mode
		# self.MODE = os.environ.get('mode', 'default').lower()
		super(globalSettings, self).__init__('default')

	# runSetupScript handles all constants which need to be
	def setup(self):
	# found by lookups in env variable or other means
		self.set({
			'ARK_ROOT': os.environ.get('ARK_ROOT'),
			'ARK_CONFIG': os.environ.get('ARK_CONFIG'),
			'ARK_PYTHON': os.environ.get('ARK_PYTHON'),
			'ARK_PYTHONLIB': os.environ.get('ARK_PYTHONLIB'),
		})

		if 'ARK_CURRENT_APP' in os.environ:
			self.settings['ARK_CURRENT_APP'] = \
				os.environ['ARK_CURRENT_APP'].lower()
		else:
			self.settings['ARK_CURRENT_APP'] = 'standalone'

		self.setSharedRoot()
		self.setAssetsRoot()
		self.setComputerInfo()
		self.setNetworkInfo()
		self.setTempFolder()

	# handle WIN/LINUX paths
	# if this computer is Linux, find all *_LINUX keys in self.settings
	# and modify to regular
	# if computers, find all *_WIN keys and modify to regular
	# NUKE_ROOT_WIN and NUKE_ROOT_LINUX --> NUKE_ROOT
	def handlePlatforms(self):
		if cOS.isWindows():
			for key, value in self.settings.iteritems():
				if key.endswith('_WIN'):
					newKey = key[:-4]
					self.settings[newKey] = value
		elif cOS.isLinux():
			for key, value in self.settings.iteritems():
				if key.endswith('_LINUX'):
					newKey = key[:-6]
					self.settings[newKey] = value
		else:
			raise Exception('Not yet applicable for operating system:', sys.platform)

	# Override inherited function updateFromFile to additionally call
	# handlePlatforms - resolving Linux/Windows vars
	def updateFromFile(self, filename):
		with open(filename) as f:
			settings = arkUtil.parseJSON(f)
			self.updateSettings(settings)
		self.handlePlatforms()

	# overrideSettings gets overriden as global settings does
	# not follow the <app>.<user>.json naming conventino
	def overrideSettings(self):
		if self.MODE == 'default':
			return
		try:
			settingsFile = self.rootDir + self.MODE + '.json'
			self.updateFromFile(settingsFile)
		except:
			pass

	# Set ramburglar shared drive root
	def setSharedRoot(self):
		if self.settings.get('SHARED_ROOT'):
			# do nothing since it's already set
			pass
		elif 'ARK_SHARED_ROOT' in os.environ:
			self.settings['SHARED_ROOT'] = \
				os.environ.get('ARK_SHARED_ROOT')
		elif cOS.isWindows():
			self.settings['SHARED_ROOT'] = \
				'r:/'
		elif cOS.isMac():
			self.settings['SHARED_ROOT'] = \
				'/Volumes/rambuglar_work/'
		elif cOS.isLinux():
			self.settings['SHARED_ROOT'] = \
				'/mnt/ramb/'

		# print 'SHARED_ROOT:', \
		# 	self.settings['SHARED_ROOT']

	# Set raidcharles assets drive root
	def setAssetsRoot(self):
		if self.settings.get('ASSETS_ROOT'):
			# do nothing since it's already set
			pass
		elif 'ARK_ASSETS_ROOT' in os.environ:
			self.settings['ASSETS_ROOT'] = \
				os.environ.get('ARK_ASSETS_ROOT')
		elif cOS.isWindows():
			self.settings['ASSETS_ROOT'] = \
				'q:/'
		elif cOS.isMac():
			self.settings['ASSETS_ROOT'] = \
				'/Volumes/raidcharles/work/'
		elif cOS.isLinux():
			self.settings['ASSETS_ROOT'] = \
				'/mnt/raid/work/'

		# print 'ASSETS_ROOT:', \
		# 	self.settings['ASSETS_ROOT']

	def setComputerInfo(self):
		if cOS.isWindows():
			# cross platform user root
			self.settings['USER_ROOT'] = \
				cOS.normalizeDir(os.path.expanduser('~'))
			self.settings['OS_USERNAME'] = \
				os.environ.get('USERNAME')
			self.settings['COMPUTER_NAME'] = \
				os.environ.get('COMPUTERNAME')
			self.settings['UNIQUE_NAME'] = \
				os.environ.get('ARK_COMPUTER_NAME')

			# Get the comp type from environment variable or guess if it's missing
			if 'COMPUTER_TYPE' in os.environ:
				self.settings['COMPUTER_TYPE'] = \
					os.environ.get('COMPUTER_TYPE')
			elif 'RENDER' in os.environ['COMPUTERNAME']:
				self.settings['COMPUTER_TYPE'] = 'render'
			elif os.path.exists(os.environ.get('ARK_ROOT') + 'ark/.git'):
				self.settings['COMPUTER_TYPE'] = 'developer'
			else:
				self.settings['COMPUTER_TYPE'] = 'workstation'

			self.settings['IS_NODE'] = \
				self.settings['COMPUTER_TYPE'] in self.nodeTypes
			self.settings['COMPUTER_LOCATION'] = \
				os.environ.get('COMPUTER_LOCATION', 'local')
		elif cOS.isLinux() or cOS.isMac():
			# cross platform user root
			self.settings['USER_ROOT'] = \
				cOS.normalizeDir(os.path.expanduser('~'))
			self.settings['OS_USERNAME'] = \
				os.environ.get('USER')
			self.settings['COMPUTER_NAME'] = \
				os.environ.get('HOSTNAME')
			self.settings['UNIQUE_NAME'] = \
				os.environ.get('ARK_COMPUTER_NAME')

			# Get the comp type from environment variable or guess if it's missing
			if 'COMPUTER_TYPE' in os.environ:
				self.settings['COMPUTER_TYPE'] = \
					os.environ.get('COMPUTER_TYPE')
			elif 'RENDER' in os.environ['HOSTNAME']:
				self.settings['COMPUTER_TYPE'] = 'render'
			else:
				self.settings['COMPUTER_TYPE'] = 'workstation'

			self.settings['IS_NODE'] = \
				self.settings['COMPUTER_TYPE'] in self.nodeTypes
			self.settings['COMPUTER_LOCATION'] = \
				os.environ.get('COMPUTER_LOCATION', 'local')

	def setNetworkInfo(self):
		pass
		# elif self.settings['COMPUTER_LOCATION'] != 'local':
		# 	self.settings['DATABASE_ROOT'] = '108.60.58.20'
		# else:
		# 	self.settings['DATABASE_ROOT'] = '192.168.0.75'
		# self.settings['DATABASE'] = \
		# 	'http://' + self.settings['DATABASE_ROOT'] + '/api'

	def setTempFolder(self):
		if 'TEMP' in self.settings and \
			self.settings['TEMP'] is not None:
			# do nothing since it's already set
			pass
		elif 'ARK_TEMP' in os.environ:
			self.settings['TEMP'] = \
				os.environ.get('ARK_TEMP')
		elif cOS.isWindows():
			self.settings['TEMP'] = \
				'c:/temp/'
		elif cOS.isMac() or cOS.isLinux():
			self.settings['TEMP'] = \
				'/var/temp/'

		# ensure the temp directory exists
		cOS.makeDirs(self.settings['TEMP'])

	def set(self, key, value=None):
		'''
		Set for globalSettings is different
		as it doesn't save the settings.

		Use a regular SettingsManager if you
		want to save application-specific settings
		'''
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
