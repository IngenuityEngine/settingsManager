import unittest
import sys
import os
sys.path.insert(0, '../..')
from settingsManager import SettingsManager

class genericSettingsTest(unittest.TestCase):

	def setUp(self):
		os.environ['ARK_CONFIG'] = 'c:/ie/settingsManager/config'

	def tearDown(self):
		del os.environ['ARK_CONFIG']

	def test_shouldRetrieveLiteralString(self):
		appSettings = SettingsManager('testapp')
		self.assertEqual(appSettings.ONE_THING, 'APPTHING')

	def test_shouldRetrieveLiteralList(self):
		appSettings = SettingsManager('testapp')
		self.assertEqual(appSettings.ADDITIONAL_TOOLS, ['arkHelpers', 'shepherd', 'cOS', 'translators', 'weaver', 'settingsManager'])

	def test_shouldRetrieveLiteralDict(self):
		appSettings = SettingsManager('testapp')
		self.assertEqual(appSettings.JOB_LIST_TYPE, {'blacklist': 1, 'whitelist': 2})

	def test_shouldRetrieveSubstitutedString(self):
		appSettings = SettingsManager('testapp')
		self.assertEqual(appSettings.MANTRA_EXE, 'C:/Program Files/Side Effects Software/Houdini 13.0.547/bin/mantra.exe')

	def test_shouldAcceptDotAndGetNotation(self):
		appSettings = SettingsManager('testapp')
		self.assertEqual(appSettings.UNIVERSAL_ROOT, appSettings.get('UNIVERSAL_ROOT'))

	def test_shouldBeAbleToOverrideSettings(self):
		appSettings = SettingsManager('testapp', 'testuser')
		self.assertEqual(appSettings.NETWORK_TOOLSETS, 'networktools')

	def test_shouldBeAbleToAddOverrideSettings(self):
		appSettings = SettingsManager('testapp', 'testuser')
		self.assertEqual(appSettings.DUMMY_ATTR, 'dummy')

if __name__ == '__main__':
	unittest.main()


