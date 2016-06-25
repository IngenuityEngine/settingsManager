
# Standard modules
##################################################
import json

# Our modules
##################################################
import arkInit
arkInit.init()
from database import Database
import tryout

from settingsManager import DatabaseSettingsManager

databaseUrl = 'http://127.0.0.1:80/api/'


class test(tryout.TestSuite):

	testUserName = '__testUser_2142r3wsdf'

	def setUpClass(self):
		# Note: different port number is because database
		# is being run from caretaker which is where the
		# entitydef for settings lives
		self.database = Database(databaseUrl, keepTrying=True)
		self.database.connect()
		# create a testing user
		self.database.create(
			'user',
			{'name': self.testUserName})\
			.execute()
		# get the user's id
		self.userId = self.database\
			.find('user')\
				.where('name','is',self.testUserName)\
					.execute()[0]['_id']

		self.database.create('settings', {
			'key': 'Test_DBSM',
			'settings': json.dumps(
						{
							'initialFile': 'someFile.txt',
							'NumberPublished': 1,
							'Directory': 'someDirectory/'
						})
			}).execute()

		self.database.create('settings', {
			'key': 'Test_DBSM',
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

	def tearDownClass(self):
		self.database = Database(databaseUrl)
		self.database.connect()
		self.database.remove('settings').multiple(True).execute()
		self.database.remove('user').where('name','is',self.testUserName).execute()

	def setUp(self):
		self.database = Database(databaseUrl)
		self.database.connect()

	def tearDown(self):
		pass

	def test_shouldLoadDefaultSettings(self):
		self.databaseSettings = DatabaseSettingsManager(self.database, 'Test_DBSM')
		self.assertEqual(self.databaseSettings.initialFile, 'someFile.txt')
		self.assertEqual(self.databaseSettings.NumberPublished, 1)

	def test_shouldLoadSpecificSettings(self):
		self.databaseSettings = DatabaseSettingsManager(self.database, 'Test_DBSM', self.userId)
		self.assertEqual(self.databaseSettings.initialFile, 'someFile.txt')
		self.assertEqual(self.databaseSettings.NumberPublished, 2)
		self.assertEqual(self.databaseSettings.Directory, 'SomeOtherDirectory')
		self.assertEqual(self.databaseSettings.visible_fields, ['color', 'fileSize', 'stuff'])

	def test_shouldGetSetting(self):
		self.databaseSettings = DatabaseSettingsManager(self.database, 'Test_DBSM', self.userId)
		self.assertEqual(self.databaseSettings.visible_fields[1], 'fileSize')

	def test_shouldSetSetting(self):
		self.databaseSettings = DatabaseSettingsManager(self.database, 'Test_DBSM')
		self.databaseSettings.set('errorLog', 'c:/fileOfStupidity.txt')
		self.assertEqual(self.databaseSettings.errorLog, 'c:/fileOfStupidity.txt')

	def test_shouldSaveSettings(self):
		self.databaseSettings = DatabaseSettingsManager(self.database, 'Test_DBSM', self.userId)
		self.databaseSettings.set('background', 'green')
		self.databaseSettings.save()
		self.database = Database(databaseUrl)
		newSettings = DatabaseSettingsManager(self.database, 'Test_DBSM', self.userId)
		self.assertEqual(newSettings.background, 'green')

	def test_shouldCreateSettings(self):
		self.databaseSettings = DatabaseSettingsManager(self.database, 'RandomApp', self.userId)
		self.databaseSettings.set('stuffy', 'blahblah')
		self.databaseSettings.save()
		otherSettings = DatabaseSettingsManager(self.database, 'RandomApp', self.userId)
		self.assertEqual(otherSettings.stuffy, 'blahblah')


if __name__ == '__main__':
	tryout.run(test)
