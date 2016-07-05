import os
# import sys

from SettingsManager import SettingsManager
import arkInit
arkInit.init()
# import arkUtil
import cOS


class globalSettings(SettingsManager):

	nodeTypes = ['render']
	setKeysOnClass = True

	def __init__(self):

		self.MODE = os.environ.get('ARK_MODE', 'default').lower()

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
		self.setComputerInfo()
		self.setNetworkInfo()
		self.setTempFolder()

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
				'/mnt/ramburglar/'

		# print 'SHARED_ROOT:', \
		# 	self.settings['SHARED_ROOT']

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
		if self.MODE == 'test':
			self.settings['DATABASE'] = 'http://127.0.0.1'
		elif self.settings['COMPUTER_LOCATION'] != 'local':
			self.settings['DATABASE'] = 'http://108.60.58.20'
		else:
			self.settings['DATABASE'] = 'http://192.168.0.75'
		self.settings['DATABASE'] += '/api'

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
