import unittest
import sys
import json

sys.path.append('c:/ie/ark/tools/settingsManager')
sys.path.append('c:/dev/coren/python')

from coren import Coren
from settingsManager import SettingsManager

corenUrl = 'http://localhost:2020/api/'



class databaseSettingsManagerTest(unittest.TestCase):


	@classmethod
	def setUpClass(self):
		#Note: different port number is because coren is being run from caretaker
		# which is where the entitydef for settings lives
		coren = Coren(corenUrl)
		coren.create('_user', {'name': 'TestingUser'}).execute()
		userId = coren.find('_user').where('name','is','TestingUser').execute().json()[0]['_id']
		coren.create('settings', {
			'key': 'PublishManager',
			'settings': json.dumps(
						{
							'initialFile': 'someFile.txt',
							'NumberPublished': 1,
							'Directory': 'someDirectory/'
						})
			}).execute()
		coren.create('settings', {
			'key': 'PublishManager',
			'user':  userId,
			'settings':	json.dumps(
						{
							'visible_fields': ['color', 'fileSize', 'stuff'],
							'NumberPublished': 2,
							'Directory': 'SomeOtherDirectory'
						})
			}).execute()
		coren.create('settings', {
			'key': 'DifferentApp',
			'settings': json.dumps(
				{
					'preference': 'well done',
					'yogurt': 'strawberry',

				})
			})

	@classmethod
	def tearDownClass(self):
		coren = Coren(corenUrl)
		coren.delete('settings').execute()
		coren.delete('settings').execute()
		coren.delete('_user').where('name','is','TestingUser').execute()

	@classmethod
	def setUp(self):
		coren = Coren(corenUrl)
		self.databaseSettings = SettingsManager('database', coren)

	@classmethod
	def tearDown(self):
		pass

	def test_dummy(self):
		pass

	def test_shouldLoadDefaultSettings(self):
		self.databaseSettings.load('PublishManager')
		self.assertEqual(self.databaseSettings.getSetting('initialFile'), 'someFile.txt')
		self.assertEqual(self.databaseSettings.getSetting('NumberPublished'), 1)

	def test_shouldLoadSpecificSettings(self):
		self.databaseSettings.load('PublishManager', 'TestingUser')
		self.assertEqual(self.databaseSettings.getSetting('initialFile'), 'someFile.txt')
		self.assertEqual(self.databaseSettings.getSetting('NumberPublished'), 2)
		self.assertEqual(self.databaseSettings.getSetting('Directory'), 'SomeOtherDirectory')
		self.assertEqual(self.databaseSettings.getSetting('visible_fields'), ['color', 'fileSize', 'stuff'])

	def test_shouldGetSetting(self):
		self.databaseSettings.load('PublishManager', 'TestingUser')
		self.assertEqual(self.databaseSettings.getSetting('visible_fields')[1], 'fileSize')

	def test_shouldSetSetting(self):
		self.databaseSettings.load('PublishManager')
		self.databaseSettings.setSetting('errorLog', 'c:/fileOfStupidity.txt')
		self.assertEqual(self.databaseSettings.getSetting('errorLog'), 'c:/fileOfStupidity.txt')


	def test_shouldSaveSettings(self):
		self.databaseSettings.load('PublishManager', 'TestingUser')
		self.databaseSettings.setSetting('background', 'green')
		self.databaseSettings.saveSettings()
		coren = Coren(corenUrl)
		newSettings = SettingsManager('database', coren)
		newSettings.load('PublishManager', 'TestingUser')
		self.assertEqual(newSettings.getSetting('background'), 'green')
		newSettings.load('PublishManager')
		self.assertTrue('background' not in newSettings.getSettings())

	def test_shouldCreateSettings(self):
		self.databaseSettings.create('randomThing')
		self.databaseSettings.setSetting('stuffy', 'blahblah')
		self.databaseSettings.saveSettings()
		self.databaseSettings.create('randomThing', 'TestingUser')


if __name__ == '__main__':
	unittest.main()