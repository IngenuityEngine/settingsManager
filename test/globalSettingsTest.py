import unittest
import sys
import os
sys.path.insert(0, '..')
from settingsManager import globalSettings

class globalSettingsTest(unittest.TestCase):

	def setUp(self):
		os.environ['ARK_CONFIG'] = 'c:/ie/settingsManager/config'
		os.environ['ARK_MODE'] = 'default'

	def tearDown(self):
		os.environ['ARK_CONFIG'] = 'c:/ie/config'

	def test_shouldRetrieveLiteralString(self):
		arkGlobals = globalSettings()
		self.assertEqual(arkGlobals.IETEMP, 'C:/ie/temp/')

	def test_shouldRetrieveLiteralList(self):
		arkGlobals = globalSettings()
		self.assertEqual(arkGlobals.ADDITIONAL_TOOLS, ['arkHelpers', 'shepherd', 'cOS', 'translators', 'weaver', 'settingsManager'])

	def test_shouldRetrieveLiteralDict(self):
		arkGlobals = globalSettings()
		self.assertEqual(arkGlobals.JOB_LIST_TYPE, {'blacklist': 1, 'whitelist': 2})

	def test_shouldRetrieveSubstitutedString(self):
		arkGlobals = globalSettings()
		self.assertEqual(arkGlobals.MANTRA_EXE, 'C:/Program Files/Side Effects Software/Houdini 13.0.547/bin/mantra.exe')

	def test_shouldRetrieveProgrammaticKey(self):
		arkGlobals = globalSettings()
		self.assertEqual(arkGlobals.ARK_ROOT, os.environ.get('ARK_ROOT'))

	def test_shouldAcceptDotAndGetNotation(self):
		arkGlobals = globalSettings()
		self.assertEqual(arkGlobals.ARK_ROOT, arkGlobals.get('ARK_ROOT'))
		self.assertEqual(arkGlobals.get('ARK_ROOT'), os.environ.get('ARK_ROOT'))

	def test_shouldBeAbleToOverrideSettings(self):
		os.environ['ARK_MODE'] = 'overridetest'
		arkGlobals = globalSettings()
		self.assertEqual(arkGlobals.NETWORK_TOOLSETS, 'networktools')

	def test_shouldBeAbleToOverrideSettings(self):
		os.environ['ARK_MODE'] = 'overridetest'
		arkGlobals = globalSettings()
		self.assertEqual(arkGlobals.DUMMY_ATTR, 'dummy')

if __name__ == '__main__':
	unittest.main()


