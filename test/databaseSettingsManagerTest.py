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
		database = Database(databaseUrl)
		database.create('user', {'name': 'TestingUser'}).execute()
		userId = database.find('user').where('name','is','TestingUser').execute().json()[0]['_id']
		database.create('settings', {
			'key': 'PublishManager',
			'settings': json.dumps(
						{
							'initialFile': 'someFile.txt',
							'NumberPublished': 1,
							'Directory': 'someDirectory/'
						})
			}).execute()
		database.create('settings', {
			'key': 'PublishManager',
			'user':  userId,
			'settings':	json.dumps(
						{
							'visible_fields': ['color', 'fileSize', 'stuff'],
							'NumberPublished': 2,
							'Directory': 'SomeOtherDirectory'
						})
			}).execute()
		database.create('settings', {
			'key': 'DifferentApp',
			'settings': json.dumps(
				{
					'preference': 'well done',
					'yogurt': 'strawberry',

				})
			})

	@classmethod
	def tearDownClass(self):
		database = Database(databaseUrl)
		database.remove('settings').multiple(True).execute()
		database.remove('user').where('name','is','TestingUser').execute()

	@classmethod
	def setUp(self):
		database = Database(databaseUrl)

	@classmethod
	def tearDown(self):
		pass

	def test_dummy(self):
		pass

	def test_shouldLoadDefaultSettings(self):
		self.databaseSettings = DatabaseSettingsManager('PublishManager')
		self.assertEqual(self.databaseSettings.initialFile, 'someFile.txt')
		self.assertEqual(self.databaseSettings.NumberPublished, 1)

	def test_shouldLoadSpecificSettings(self):
		self.databaseSettings = DatabaseSettingsManager('PublishManager', 'TestingUser')
		self.assertEqual(self.databaseSettings.initialFile, 'someFile.txt')
		self.assertEqual(self.databaseSettings.NumberPublished, 2)
		self.assertEqual(self.databaseSettings.Directory, 'SomeOtherDirectory')
		self.assertEqual(self.databaseSettings.visible_fields, ['color', 'fileSize', 'stuff'])

	def test_shouldGetSetting(self):
		self.databaseSettings = DatabaseSettingsManager('PublishManager' 'TestingUser')
		self.assertEqual(self.databaseSettings.visible_fields[1], 'fileSize')

	# def test_shouldSetSetting(self):
	# 	self.databaseSettings.load('PublishManager')
	# 	self.databaseSettings.setSetting('errorLog', 'c:/fileOfStupidity.txt')
	# 	self.assertEqual(self.databaseSettings.getSetting('errorLog'), 'c:/fileOfStupidity.txt')


	# def test_shouldSaveSettings(self):
	# 	self.databaseSettings.load('PublishManager', 'TestingUser')
	# 	self.databaseSettings.setSetting('background', 'green')
	# 	self.databaseSettings.saveSettings()
	# 	database = Database(databaseUrl)
	# 	newSettings = SettingsManager('database', database)
	# 	newSettings.load('PublishManager', 'TestingUser')
	# 	self.assertEqual(newSettings.getSetting('background'), 'green')
	# 	newSettings.load('PublishManager')
	# 	self.assertTrue('background' not in newSettings.getSettings())

	# def test_shouldCreateSettings(self):
	# 	self.databaseSettings.create('randomThing')
	# 	self.databaseSettings.setSetting('stuffy', 'blahblah')
	# 	self.databaseSettings.saveSettings()
	# 	self.databaseSettings.create('randomThing', 'TestingUser')


if __name__ == '__main__':
	unittest.main()