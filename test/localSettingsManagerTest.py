import unittest
import sys
import json

sys.path.append('c:/ie/ark/tools/settingsManager')
from settingsManager import SettingsManager

class localSettingsManagerTest(unittest.TestCase):

	@classmethod
	def setUp(self):
		with open('c:/settings/PublishManager.json', 'w') as SettingsFile:
				defaultSettings = {
					'default': {
							'initialFile': 'someFile.txt',
							'NumberPublished': 1,
							'Directory': 'someDirectory/'
						},
					'Grant Miller' :{
							'visible_fields': ['color', 'fileSize', 'stuff'],
							'NumberPublished': 2,
							'Directory': 'SomeOtherDirectory'
						}
					}
				json.dump(defaultSettings, SettingsFile,indent=4)
		self.localSettings = SettingsManager('local', 'c:/settings/')

	@classmethod
	def tearDown(self):
		pass

	def test_dummy(self):
		pass

	def test_shouldLoadDefaultSettings(self):
		self.localSettings.load('PublishManager')
		self.assertEqual(self.localSettings.getSetting('initialFile'), 'someFile.txt')
		self.assertEqual(self.localSettings.getSetting('NumberPublished'), 1)

	def test_shouldLoadSpecificSettings(self):
		self.localSettings.load('PublishManager', 'Grant Miller')
		self.assertEqual(self.localSettings.getSetting('initialFile'), 'someFile.txt')
		self.assertEqual(self.localSettings.getSetting('NumberPublished'), 2)
		self.assertEqual(self.localSettings.getSetting('Directory'), 'SomeOtherDirectory')
		self.assertEqual(self.localSettings.getSetting('visible_fields'), ['color', 'fileSize', 'stuff'])

	def test_shouldGetSetting(self):
		self.localSettings.load('PublishManager', 'Grant Miller')
		self.assertEqual(self.localSettings.getSetting('visible_fields')[1], 'fileSize')

	def test_shouldSetSetting(self):
		self.localSettings.load('PublishManager')
		self.localSettings.setSetting('errorLog', 'c:/fileOfStupidity.txt')
		self.assertEqual(self.localSettings.getSetting('errorLog'), 'c:/fileOfStupidity.txt')


	def test_shouldSaveSettings(self):
		self.localSettings.load('PublishManager', 'Grant Miller')
		self.localSettings.setSetting('background', 'green')
		self.localSettings.saveSettings()
		newSettings = SettingsManager('local', 'c:/settings/')
		newSettings.load('PublishManager', 'Grant Miller')
		self.assertEqual(newSettings.getSetting('background'), 'green')
		newSettings.load('PublishManager')
		self.assertTrue('background' not in newSettings.getSettings())

	def test_shouldCreateSettings(self):
		self.localSettings.create('randomThing')
		self.localSettings.setSetting('stuffy', 'blahblah')
		self.localSettings.saveSettings()
		self.localSettings.create('randomThing', 'Grant Miller')



if __name__ == '__main__':
	unittest.main()