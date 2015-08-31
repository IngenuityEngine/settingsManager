import unittest
import sys
import json

import arkInit
arkInit.init()
from database import Database

from settingsManager import DatabaseSettingsManager

databaseUrl = 'http://localhost:2160/api/'



class databaseSettingsManagerTest(unittest.TestCase):


	@classmethod
	def setUpClass(self):
		#Note: different port number is because database is being run from caretaker
		# which is where the entitydef for settings lives
		self.database = Database(databaseUrl)
		self.database.connect()
		self.database.create('user', {'name': 'TestingUser'}).execute()
		self.userId = self.database.find('user').where('name','is','TestingUser').execute()[0]['_id']
		self.database.create('settings', {
			'key': 'PublishManager',
			'settings': json.dumps(
						{
							'initialFile': 'someFile.txt',
							'NumberPublished': 1,
							'Directory': 'someDirectory/'
						})
			}).execute()
		self.database.create('settings', {
			'key': 'PublishManager',
			'user':  self.userId,
			'settings':	json.dumps(
						{
							'visible_fields': ['color', 'fileSize', 'stuff'],
							'NumberPublished': 2,
							'Directory': 'SomeOtherDirectory'
						})
			}).execute()
		self.database.create('settings', {
			'key': 'DifferentApp',
			'settings': json.dumps(
				{
					'preference': 'well done',
					'yogurt': 'strawberry',

				})
			})

	@classmethod
	def tearDownClass(self):
		self.database = Database(databaseUrl)
		self.database.connect()
		self.database.remove('settings').multiple(True).execute()
		self.database.remove('user').where('name','is','TestingUser').execute()

	@classmethod
	def setUp(self):
		self.database = Database(databaseUrl)
		self.database.connect()

	@classmethod
	def tearDown(self):
		pass

	def test_dummy(self):
		pass

	def test_shouldLoadDefaultSettings(self):
		self.databaseSettings = DatabaseSettingsManager(self.database, 'PublishManager')
		self.assertEqual(self.databaseSettings.initialFile, 'someFile.txt')
		self.assertEqual(self.databaseSettings.NumberPublished, 1)

	def test_shouldLoadSpecificSettings(self):
		self.databaseSettings = DatabaseSettingsManager(self.database, 'PublishManager', self.userId)
		self.assertEqual(self.databaseSettings.initialFile, 'someFile.txt')
		self.assertEqual(self.databaseSettings.NumberPublished, 2)
		self.assertEqual(self.databaseSettings.Directory, 'SomeOtherDirectory')
		self.assertEqual(self.databaseSettings.visible_fields, ['color', 'fileSize', 'stuff'])

	def test_shouldGetSetting(self):
		self.databaseSettings = DatabaseSettingsManager(self.database, 'PublishManager', self.userId)
		self.assertEqual(self.databaseSettings.visible_fields[1], 'fileSize')

	def test_shouldSetSetting(self):
		self.databaseSettings = DatabaseSettingsManager(self.database, 'PublishManager')
		self.databaseSettings.set('errorLog', 'c:/fileOfStupidity.txt')
		self.assertEqual(self.databaseSettings.errorLog, 'c:/fileOfStupidity.txt')


	def test_shouldSaveSettings(self):
		self.databaseSettings = DatabaseSettingsManager(self.database, 'PublishManager', self.userId)
		self.databaseSettings.set('background', 'green')
		self.databaseSettings.save()
		self.database = Database(databaseUrl)
		newSettings = DatabaseSettingsManager(self.database, 'PublishManager', self.userId)
		self.assertEqual(newSettings.background, 'green')

	def test_shouldCreateSettings(self):
		self.databaseSettings = DatabaseSettingsManager(self.database, 'RandomApp', self.userId)
		self.databaseSettings.set('stuffy', 'blahblah')
		self.databaseSettings.save()
		otherSettings = DatabaseSettingsManager(self.database, 'RandomApp', self.userId)
		self.assertEqual(otherSettings.stuffy, 'blahblah')


if __name__ == '__main__':
	unittest.main()