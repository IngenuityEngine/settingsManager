import os
import sys
from types import *
import commentjson as json


class globalSettings(object):
	def __init__(self, overrides=None):
		super(globalSettings, self).__init__()
		self.settings = {}
		self.rootDir = os.environ.get('ARK_CONFIG', os.getcwd())
		self.load()
		self.runComputerSetup()
		self.overrides()
		for key in self.settings:
			setattr(self, key, self.get(key))

	def get(self, key):
		if key in self.settings:
				lookup = self.settings[key]
				return self.formatAnswer(lookup)
		else:
			raise KeyError('%s is not a global setting!' % key)

	def load(self):
		with open(self.rootDir+'/default.json') as f:
			self.settings = json.load(f)
		except:
			raise IOError(self.rootDir+'/default.json could not be found!')

	def formatAnswer(self, key):
		keyType = type(key)
		if isinstance(key, StringTypes):
			return str(key.format(**self.settings))
		elif keyType == ListType:
			return [self.formatAnswer(x) for x in key]
		elif keyType == DictType:
			return {x: self.formatAnswer(key[x]) for x in key}
		else:
			return key

	def overrides(self):
		arkMode = os.environ.get('ARK_MODE', None)
		if arkMode:
			with open(self.rootDir+'/'+ arkMode + '.json') as f:
				extraSettings = json.load(f)
				self.settings.update(extraSettings)
			except:
				pass


	#runComputerSetup handles all constants which need to be found by lookups in env variable or other means
	def runComputerSetup(self):
		self.settings['ARK_ROOT'] = os.environ.get('ARK_ROOT')
		# Tools root is up a dir from wherever ark is installed
		self.settings['TOOLS_ROOT'] = '/'.join(self.settings['ARK_ROOT'].split('/')[:-2])+'/'

		#OS Setup
		#########################################################
		OS = 'windows'
		if sys.platform == 'darwin':
			OS = 'mac'
		elif sys.platform == 'linux2':
			OS = 'linux'
		self.settings['OS'] = OS
		if 'ROOT' in os.environ:
			ROOT = os.getenv('ROOT')
		elif sys.platform == 'win32':
			ROOT = 'R:/'
		else:
			# fix: who knows, stupid macs
			raise Exception('Invalid system type: ' + sys.platform)
			ROOT = 'volumes/raidcharles/'
		self.settings['ROOT'] = ROOT
		self.settings['LOCAL_USERNAME'] = os.environ.get('USERNAME')
		if OS =='windows':
			self.settings['USERROOT'] = 'c:/users/{LOCAL_USERNAME}/'
		self.settings['COMPUTER_NAME'] = os.getenv('COMPUTER_NAME')

		# Computer Setup
		###############################################################
		# Get the comp typ from environment variable or guess if it's missing
		if 'COMPUTER_TYPE' in os.environ:
			self.settings['COMPUTER_TYPE'] = os.getenv('COMPUTER_TYPE')
		elif 'RENDER' in os.environ['COMPUTERNAME']:
			COMPUTER_TYPE = 'renderNode'
		else:
			COMPUTER_TYPE = 'workstation'
		self.settings['COMPUTER_TYPE'] = COMPUTER_TYPE

		self.settings['IS_NODE'] = (COMPUTER_TYPE in ['renderNode', 'ec2'])
		self.settings['COMPUTER_LOCATION'] = os.environ.get('COMPUTER_LOCATION', 'local')

		#Network Setup
		###############################################################
		self.settings['DATABASE_HOST'] = '108.60.58.20' if COMPUTER_TYPE == 'ec2' else '192.168.0.99'

		#Program Paths
		##############################################################
		self.settings['ARK_CURRENT_APP'] = os.environ['ARK_CURRENT_APP'].lower() if 'ARK_CURRENT_APP' in os.environ else None

		self.settings['programs'] = os.listdir(self.settings['programsRoot'])
		self.settings['programs'].sort()

		# Do some extra legwork for Nuke as it changes all the time
		self.settings['NUKE_EXE'] = '{programsRoot}{nuke_version}/'+self.settings['nuke_version'].split('.')[0]+'.0.exe'
		self.settings['nukePath'] = os.environ.get('NUKE_PATH')
		if self.settings['nukePath']:
			self.settings['NETWORK_TOOLSETS'] = '{nukePath}/ToolSets'

def init():
	return globalSettings()






