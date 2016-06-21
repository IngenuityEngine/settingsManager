import os
# import sys

from SettingsManager import SettingsManager
import arkInit
arkInit.init()
import arkUtil
import cOS


class globalSettings(SettingsManager):

	nodeTypes = ['render']

	def __init__(self):
		super(globalSettings, self).__init__('default')

	# overrideSettings gets overriden as global settings does
	# not follow the <app>.<user>.json naming conventino
	def overrideSettings(self):
		arkMode = os.environ.get('ARK_MODE', None)
		if not arkMode:
			return
		try:
			settingsFile = self.rootDir + '/' + arkMode + '.json'
			with open(settingsFile) as f:
				extraSettings = arkUtil.parseJSON(f)
				self.updateSettings(extraSettings)
		except:
			pass

	def setSharedRoot(self):
		if 'ARK_SHARED_ROOT' in self.settings and \
			self.settings['ARK_SHARED_ROOT'] is not None:
			# do nothing since it's already set
			pass
		elif 'ARK_SHARED_ROOT' in os.environ:
			self.settings['ARK_SHARED_ROOT'] = \
				os.environ.get('ARK_SHARED_ROOT')
		elif cOS.isWindows():
			self.settings['ARK_SHARED_ROOT'] = \
				'r:/'
		elif cOS.isMac():
			self.settings['ARK_SHARED_ROOT'] = \
				'/Volumes/rambuglar_work/'
		elif cOS.isLinux():
			self.settings['ARK_SHARED_ROOT'] = \
				'/mnt/ramburglar/'

		# print 'ARK_SHARED_ROOT:', \
		# 	self.settings['ARK_SHARED_ROOT']

	def setComputerInfo(self):
		# cross platform user root
		self.settings['USERROOT'] = \
			cOS.unixPath(os.path.expanduser('~'))
		self.settings['LOCAL_USERNAME'] = \
			os.environ.get('USERNAME')
		self.settings['COMPUTER_NAME'] = \
			os.environ.get('COMPUTERNAME')

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

	def setNetworkInfo(self):
		if self.settings['COMPUTER_LOCATION'] != 'local':
			self.settings['DATABASE'] = '108.60.58.20'
		else:
			self.settings['DATABASE'] = '192.168.0.75'

	# runSetupScript handles all constants which need to be
	def setup(self):
	# found by lookups in env variable or other means
		self.set('ARK_ROOT', os.environ.get('ARK_ROOT'))
		if 'ARK_CURRENT_APP' in os.environ:
			self.settings['ARK_CURRENT_APP'] = \
				os.environ['ARK_CURRENT_APP'].lower()
		else:
			self.settings['ARK_CURRENT_APP'] = 'standalone'

		self.setSharedRoot()
		self.setComputerInfo()
		self.setNetworkInfo()

