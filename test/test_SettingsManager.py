# Standard modules
import os

# Ark modules
import arkInit
arkInit.init()
import settingsManager
import tryout
import cOS

class test(tryout.TestSuite):
	title = 'test/test_SettingsManager.py'

	def setUpClass(self):
		sourcePath = cOS.getDirName(__file__) + 'testSettings'
		self.configPath = cOS.getDirName(__file__) + 'config'
		cOS.copyTree(sourcePath, self.configPath)

	def setUp(self):
		self.ogConfig = os.environ.get('ARK_CONFIG')
		self.ogMode = os.environ.get('ARK_MODE')
		configPath = cOS.getDirName(__file__) + 'config'
		os.environ['ARK_CONFIG'] = configPath
		os.environ['ARK_MODE'] = 'default'

	def tearDown(self):
		if self.ogConfig:
			os.environ['ARK_CONFIG'] = self.ogConfig
		if self.ogMode:
			os.environ['ARK_MODE'] = self.ogMode

	def retrieveLiteralString(self):
		settings = settingsManager.getSettings()
		self.assertEqual(
			settings.firstTest, 'testOne')

	def retrieveLiteralList(self):
		settings = settingsManager.getSettings()
		self.assertEqual(
			settings.listTest,
			[
				'apples',
				'pears'
			])

	def retrieveLiteralDict(self):
		settings = settingsManager.getSettings()
		self.assertEqual(
			settings.dictTest,
			{'other': 'test'})

	def retrieveSubstitutedString(self):
		settings = settingsManager.getSettings()
		self.assertEqual(
			settings.subTest,
			'testOne/testTwo')

	def dotAndGetNotation(self):
		settings = settingsManager.getSettings()
		self.assertEqual(
			settings.firstTest,
			settings.get('firstTest'))

	def loadAppSettings(self):
		settings = settingsManager.getSettings('sweetApp')
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
		settings = settingsManager.getSettings()
		self.assertEqual(
			settings.urlTest,
			'http://192.168.0.75/api')

	def overrideSettingsWithUser(self):
		settings = settingsManager.getSettings('sweetApp',
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

	def setASettingAndSaveForANewUser(self):
		settings = settingsManager.getSettings('sweetApp',
			'newUser')
		settings.set('autoRun', False)

		settings = settingsManager.getSettings('sweetApp',
			'newUser')
		self.assertEqual(settings.autoRun, False)
		self.assertTrue(os.path.isfile(settings.filename))

	def setASettingAndSaveForExistingUser(self):
		settings = settingsManager.getSettings('sweetApp',
			'blented')
		settings.set('awesome', True)

		settings = settingsManager.getSettings('sweetApp',
			'blented')
		self.assertEqual(settings.awesome, True)
		self.assertTrue(os.path.isfile(settings.filename))


if __name__ == '__main__':
	tryout.run(test)
