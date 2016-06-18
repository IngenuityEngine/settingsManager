# Standard modules
import os

# Ark modules
import arkInit
arkInit.init()
from settingsManager import SettingsManager
import tryout
import cOS

class test(tryout.TestSuite):
	title = 'test/test_SettingsManager.py'

	def setUp(self):
		self.ogConfig = os.environ.get('ARK_CONFIG')
		self.ogMode = os.environ.get('ARK_MODE')
		configPath = cOS.getDirName(__file__) + 'testSettings'
		os.environ['ARK_CONFIG'] = configPath
		os.environ['ARK_MODE'] = 'default'

	def tearDown(self):
		if self.ogConfig:
			os.environ['ARK_CONFIG'] = self.ogConfig
		if self.ogMode:
			os.environ['ARK_MODE'] = self.ogMode

	def retrieveLiteralString(self):
		settings = SettingsManager()
		self.assertEqual(
			settings.firstTest, 'testOne')

	def retrieveLiteralList(self):
		settings = SettingsManager()
		self.assertEqual(
			settings.listTest,
			[
				'apples',
				'pears'
			])

	def retrieveLiteralDict(self):
		settings = SettingsManager()
		self.assertEqual(
			settings.dictTest,
			{'other': 'test'})

	def retrieveSubstitutedString(self):
		settings = SettingsManager()
		self.assertEqual(
			settings.subTest,
			'testOne/testTwo')

	def dotAndGetNotation(self):
		settings = SettingsManager()
		self.assertEqual(
			settings.firstTest,
			settings.get('firstTest'))

	def loadAppSettings(self):
		settings = SettingsManager('sweetApp')
		self.assertEqual(
			settings.firstTest,
			'testModeOne')
		self.assertEqual(
			settings.listTest,
			'variable overwrite')
		self.assertEqual(
			settings.dictTest,
			{
				"more": "variables"
			})

	def handle_urls(self):
		settings = SettingsManager()
		self.assertEqual(
			settings.urlTest,
			'http://192.168.0.75/api')

	def overrideSettingsWithUser(self):
		settings = SettingsManager('sweetApp',
			'blented')
		self.assertEqual(
			settings.firstTest,
			'blented is awesome')
		self.assertEqual(
			settings.listTest,
			'variable overwrite')
		self.assertEqual(
			settings.dictTest,
			{
				"more": "variables",
				"such": "dict",
				"so": "overwrite"
			})


if __name__ == '__main__':
	tryout.run(test)
