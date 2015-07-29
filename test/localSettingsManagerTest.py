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
				json.dump(defaultSettings, SettingsFile, indent=4)
		self.localSettings = SettingsManager('local', 'c:/settings/')

	@classmethod
	def tearDown(self):
		pass

	def test_dummy(self):
		pass

	def test_shouldLoadDefaultSettings(self):
		self.localSettings.load('PublishManager')
		self.assertEqual(self.localSettings.get('initialFile'), 'someFile.txt')
		self.assertEqual(self.localSettings.get('NumberPublished'), 1)

	def test_shouldLoadSpecificSettings(self):
		self.localSettings.load('PublishManager', 'Grant Miller')
		self.assertEqual(self.localSettings.get('initialFile'), 'someFile.txt')
		self.assertEqual(self.localSettings.get('NumberPublished'), 2)
		self.assertEqual(self.localSettings.get('Directory'), 'SomeOtherDirectory')
		self.assertEqual(self.localSettings.get('visible_fields'), ['color', 'fileSize', 'stuff'])

	def test_shouldget(self):
		self.localSettings.load('PublishManager', 'Grant Miller')
		self.assertEqual(self.localSettings.get('visible_fields')[1], 'fileSize')

	def test_shouldset(self):
		self.localSettings.load('PublishManager')
		self.localSettings.set('errorLog', 'c:/fileOfStupidity.txt')
		self.assertEqual(self.localSettings.get('errorLog'), 'c:/fileOfStupidity.txt')


	def test_shouldsave(self):
		self.localSettings.load('PublishManager', 'Grant Miller')
		self.localSettings.set('background', 'green')
		self.localSettings.save()
		newSettings = SettingsManager('local', 'c:/settings/')
		newSettings.load('PublishManager', 'Grant Miller')
		self.assertEqual(newSettings.get('background'), 'green')
		newSettings.load('PublishManager')
		self.assertTrue('background' not in newSettings.get())

	def test_shouldCreateSettings(self):
		self.localSettings.create('randomThing')
		self.localSettings.set('stuffy', 'blahblah')
		self.localSettings.save()
		self.localSettings.create('randomThing', 'Grant Miller')



if __name__ == '__main__':
	unittest.main()